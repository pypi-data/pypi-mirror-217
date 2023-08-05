"""Functions related to the loading of models."""

import warnings
from json import JSONDecodeError
from typing import Any, Dict, List, Tuple, Type, Union

import torch
import torch.nn as nn
from transformers import PreTrainedModel
from transformers.configuration_utils import PretrainedConfig
from transformers.models.auto.configuration_auto import AutoConfig
from transformers.models.auto.tokenization_auto import AutoTokenizer
from transformers.models.electra.modeling_electra import (
    ElectraForQuestionAnswering,
    ElectraForSequenceClassification,
    ElectraForTokenClassification,
)
from transformers.models.xlm_roberta.modeling_xlm_roberta import (
    XLMRobertaForQuestionAnswering,
    XLMRobertaForSequenceClassification,
    XLMRobertaForTokenClassification,
)
from transformers.tokenization_utils import PreTrainedTokenizer

from .exceptions import InvalidBenchmark
from .norbert import load_norbert_model
from .utils import block_terminal_output, get_class_by_name


def load_model(
    model_id: str,
    revision: str,
    supertask: str,
    language: str,
    num_labels: int,
    id2label: List[str],
    label2id: Dict[str, int],
    from_flax: bool,
    use_auth_token: Union[bool, str],
    cache_dir: str,
    raise_errors: bool = False,
) -> Tuple[PreTrainedTokenizer, PreTrainedModel]:
    """Load a model.

    Args:
        model_id (str):
            The Hugging Face ID of the model.
        revision (str):
            The specific version of the model. Can be a branch name, a tag name, or a
            commit hash.
        supertask (str):
            The supertask of the task to benchmark the model on.
        language (str):
            The language of the dataset on which to benchmark the model.
        num_labels (int):
            The number of labels in the dataset.
        id2label (list of str):
            The mapping from ID to label.
        label2id (dict of str to int):
            The mapping from label to ID.
        from_flax (bool):
            Whether the model is a Flax model.
        use_auth_token (bool or str):
            Whether to use an authentication token to access the model. If a boolean
            value is specified then it is assumed that the user is logged in to the
            Hugging Face CLI, and if a string is specified then it is used as the
            token.
        cache_dir (str):
            The directory to cache the model in.
        raise_errors (bool, optional):
            Whether to raise errors instead of trying to fix them silently.

    Returns:
        pair of (tokenizer, model):
            The tokenizer and model.

    Raises:
        RuntimeError:
            If the framework is not recognized.
    """
    config: PretrainedConfig
    block_terminal_output()

    while True:
        try:
            # If the model ID specifies a fresh model, then load that.
            if model_id.startswith("fresh"):
                model_cls, model_id = load_fresh_model_class(
                    model_id=model_id, supertask=supertask
                )
                config = AutoConfig.from_pretrained(
                    model_id,
                    use_auth_token=use_auth_token,
                    num_labels=num_labels,
                    id2label=id2label,
                    label2id=label2id,
                    cache_dir=cache_dir,
                )
                model = model_cls(config)

            # Special handling of NorBERT3 models, as they are not included in the
            # `transformers` library yet
            elif "norbert3" in model_id:
                model = load_norbert_model(
                    model_id=model_id,
                    revision=revision,
                    supertask=supertask,
                    num_labels=num_labels,
                    id2label=id2label,
                    label2id=label2id,
                    from_flax=from_flax,
                    use_auth_token=use_auth_token,
                    cache_dir=cache_dir,
                )

            # Otherwise load the pretrained model
            else:
                try:
                    config = AutoConfig.from_pretrained(
                        model_id,
                        revision=revision,
                        use_auth_token=use_auth_token,
                        num_labels=num_labels,
                        id2label=id2label,
                        label2id=label2id,
                        cache_dir=cache_dir,
                    )
                except KeyError as e:
                    key = e.args[0]
                    raise InvalidBenchmark(
                        f"The model config for the mmodel {model_id!r} could not be "
                        f"loaded, as the key {key!r} was not found in the config."
                    )

                # Get the model class associated with the supertask
                model_cls_or_none: Union[
                    None, Type[PreTrainedModel]
                ] = get_class_by_name(
                    class_name=f"auto-model-for-{supertask}",
                    module_name="transformers",
                )

                # If the model class could not be found then raise an error
                if not model_cls_or_none:
                    raise InvalidBenchmark(
                        f"The supertask '{supertask}' does not correspond to a "
                        "Hugging Face AutoModel type (such as "
                        "`AutoModelForSequenceClassification`)."
                    )

                # If the model is a DeBERTaV2 model then we ensure that
                # `pooler_hidden_size` is the same size as `hidden_size`
                if config.model_type == "deberta-v2":
                    config.pooler_hidden_size = config.hidden_size

                # Load the model
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=UserWarning)
                    model_or_tuple = model_cls_or_none.from_pretrained(
                        model_id,
                        revision=revision,
                        use_auth_token=use_auth_token,
                        config=config,
                        cache_dir=cache_dir,
                        from_flax=from_flax,
                        ignore_mismatched_sizes=True,
                    )
                if isinstance(model_or_tuple, tuple):
                    model = model_or_tuple[0]
                else:
                    model = model_or_tuple

            # Break out of the loop
            break

        except (OSError, ValueError) as e:
            # If `from_flax` is False but only Flax models are available then try again
            # with `from_flax` set to True
            if not from_flax and "Use `from_flax=True` to load this model" in str(e):
                from_flax = True
                continue

            # Deal with the case where the checkpoint is incorrect
            if "checkpoint seems to be incorrect" in str(e):
                raise InvalidBenchmark(
                    f"The model {model_id!r} has an incorrect checkpoint."
                )

            # Otherwise raise a more generic error
            raise InvalidBenchmark(
                f"The model {model_id} either does not exist on the Hugging Face Hub, "
                "or it has no frameworks registered, or it is a private model. If "
                "it *does* exist on the Hub and is a public model then please "
                "ensure that it has a framework registered. If it is a private "
                "model then enable the `--use-auth-token` flag and make sure that "
                "you are logged in to the Hub via the `huggingface-cli login` command."
            )

    # If the model is of type XMOD then we need to set the default language
    if "XMOD" in type(model).__name__:
        language_mapping = dict(
            da="da_DK",
            sv="sv_SE",
            nb="no_XX",
            nn="no_XX",
            no="no_XX",
        )
        if language not in language_mapping:
            raise InvalidBenchmark(
                f"The language {language!r} is not supported by the XMOD model."
            )
        model.set_default_language(language_mapping[language])

    # Set up the model for question answering
    if supertask == "question-answering":
        model = setup_model_for_question_answering(model=model)

    # Load the tokenizer. If the model is a subclass of a RoBERTa model then we have to
    # add a prefix space to the tokens, by the way the model is constructed.
    prefix_models = ["Roberta", "GPT", "Deberta"]
    prefix = any(model_type in type(model).__name__ for model_type in prefix_models)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        try:
            tokenizer: PreTrainedTokenizer = AutoTokenizer.from_pretrained(
                model_id,
                revision=revision,
                use_auth_token=use_auth_token,
                add_prefix_space=prefix,
                cache_dir=cache_dir,
                use_fast=True,
                verbose=False,
            )
        except (JSONDecodeError, OSError):
            raise InvalidBenchmark(f"Could not load tokenizer for model {model_id!r}.")

    # Align the model and the tokenizer
    model, tokenizer = align_model_and_tokenizer(
        model=model, tokenizer=tokenizer, raise_errors=raise_errors
    )

    return tokenizer, model


def load_fresh_model_class(
    model_id: str, supertask: str
) -> Tuple[Type[PreTrainedModel], str]:
    """Load a fresh model class.

    Args:
        model_id (str):
            The Hugging Face ID of the model.
        supertask (str):
            The supertask of the task to benchmark the model on.

    Returns:
        pair of Type[PreTrainedModel] and str:
            The model class and the pretrained model ID.
    """
    if model_id == "fresh-xlmr-base":
        model_id = "xlm-roberta-base"
        if supertask == "sequence-classification":
            model_cls = XLMRobertaForSequenceClassification
        elif supertask == "token-classification":
            model_cls = XLMRobertaForTokenClassification
        elif supertask == "question-answering":
            model_cls = XLMRobertaForQuestionAnswering
        else:
            raise InvalidBenchmark(
                f"Supertask {supertask} is not supported for model {model_id}"
            )

    elif model_id == "fresh-electra-small":
        model_id = "google/electra-small-discriminator"
        if supertask == "sequence-classification":
            model_cls = ElectraForSequenceClassification
        elif supertask == "token-classification":
            model_cls = ElectraForTokenClassification
        elif supertask == "question-answering":
            model_cls = ElectraForQuestionAnswering
        else:
            raise InvalidBenchmark(
                f"Supertask {supertask} is not supported for model {model_id}"
            )

    else:
        raise InvalidBenchmark(
            f"A fresh model was chosen, `{model_id}`, but it was not recognized."
        )

    return model_cls, model_id


def get_children_of_module(
    name: str, module: nn.Module
) -> Union[nn.Module, Dict[str, Any], None]:
    """Get the children of a module.

    Args:
        name (str):
            The name of the module.
        module (nn.Module):
            The module to get the children of.

    Returns:
        Union[nn.Module, Dict[str, Any], None]:
            The children of the module, or None if the module has no children.
    """
    if len(list(module.children())) == 0:
        if name == "token_type_embeddings":
            return module
        else:
            return None
    else:
        submodules = dict()
        for subname, submodule in module.named_children():
            children = get_children_of_module(name=subname, module=submodule)
            if children:
                submodules[subname] = children
        return submodules


def setup_model_for_question_answering(model: PreTrainedModel) -> PreTrainedModel:
    """Setup a model for question answering.

    Args:
        model (PreTrainedModel):
            The model to setup.

    Returns:
        PreTrainedModel:
            The setup model.
    """

    # Get the models' token type embedding children, if they exist
    children = get_children_of_module(name="model", module=model)

    # If the model has token type embeddings then get them
    if children:
        # Get the list of attributes that are token type embeddings
        attribute_list = list()
        done = False
        while not done:
            for key, value in children.items():
                attribute_list.append(key)
                if isinstance(value, dict):
                    children = value
                else:
                    done = True
                break

        # Get the token type embeddings
        token_type_embeddings = model
        for attribute in attribute_list:
            token_type_embeddings = getattr(token_type_embeddings, attribute)

        # If the token type embeddings has shape (1, ...) then set the shape to
        # (2, ...) by randomly initializing the second token type embedding
        if token_type_embeddings.weight.data.shape[0] == 1:
            token_type_embeddings.weight.data = torch.cat(
                (
                    token_type_embeddings.weight.data,
                    torch.rand_like(token_type_embeddings.weight.data),
                ),
                dim=0,
            )
            token_type_embeddings.num_embeddings = 2

        # Set the model config to use the new type vocab size
        model.config.type_vocab_size = 2

    return model


def align_model_and_tokenizer(
    model: PreTrainedModel, tokenizer: PreTrainedTokenizer, raise_errors: bool = False
) -> Tuple[PreTrainedModel, PreTrainedTokenizer]:
    """Aligns the model and the tokenizer.

    Args:
        model (PreTrainedModel):
            The model to fix.
        tokenizer (PreTrainedTokenizer):
            The tokenizer to fix.
        raise_errors (bool, optional):
            Whether to raise errors instead of trying to fix them silently.

    Returns:
        pair of (model, tokenizer):
            The fixed model and tokenizer.
    """
    # Get all possible maximal lengths
    all_max_lengths: List[int] = []

    # Add the registered max length of the tokenizer
    if hasattr(tokenizer, "model_max_length") and tokenizer.model_max_length < 100_000:
        all_max_lengths.append(tokenizer.model_max_length)

    # Add the max length derived from the position embeddings
    if (
        hasattr(model.config, "max_position_embeddings")
        and hasattr(tokenizer, "pad_token_id")
        and tokenizer.pad_token_id is not None
    ):
        all_max_lengths.append(
            model.config.max_position_embeddings - tokenizer.pad_token_id - 1
        )

    # Add the max length derived from the model's input sizes
    if hasattr(tokenizer, "max_model_input_sizes"):
        all_max_lengths.extend(
            [
                size
                for size in tokenizer.max_model_input_sizes.values()
                if size is not None
            ]
        )

    # If any maximal lengths were found then use the shortest one
    if len(list(all_max_lengths)) > 0:
        min_max_length = min(list(all_max_lengths))
        tokenizer.model_max_length = min_max_length

    # Otherwise, use the default maximal length
    else:
        tokenizer.model_max_length = 512

    # If there is a mismatch between the vocab size according to the tokenizer and
    # the vocab size according to the model, we raise an error
    if hasattr(model.config, "vocab_size") and hasattr(tokenizer, "vocab_size"):
        if model.config.vocab_size < tokenizer.vocab_size:
            if raise_errors:
                raise InvalidBenchmark(
                    "The vocab size of the tokenizer is larger than the vocab size of "
                    "the model. As the --raise-errors option was specified, the "
                    "embeddings of the model will not be automatically adjusted."
                )
            model.resize_token_embeddings(new_num_tokens=tokenizer.vocab_size + 1)

    # If the tokenizer does not have a padding token (e.g. GPT-2), we use find a
    # suitable padding token and set it
    if tokenizer.pad_token is None:
        if tokenizer.eos_token is not None:
            tokenizer.padding_side = "left"
            tokenizer.pad_token = tokenizer.eos_token
            model.config.pad_token_id = tokenizer.pad_token_id
        elif tokenizer.sep_token is not None:
            tokenizer.padding_side = "left"
            tokenizer.pad_token = tokenizer.sep_token
            model.config.pad_token_id = tokenizer.pad_token_id
        else:
            raise InvalidBenchmark(
                "The tokenizer does not have a padding token and does not have a "
                "SEP token or EOS token to use as a padding token."
            )

    return model, tokenizer
