# External Packages
from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from khoj.utils.rawconfig import TextContentConfig, ConversationProcessorConfig

# Internal Packages
from khoj.utils import constants, state

import logging
import json


# Initialize Router
web_client = APIRouter()
templates = Jinja2Templates(directory=constants.web_directory)

VALID_CONTENT_TYPES = ["org", "ledger", "markdown", "pdf"]


# Create Routes
@web_client.get("/", response_class=FileResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request, "demo": state.demo})


@web_client.get("/chat", response_class=FileResponse)
def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", context={"request": request, "demo": state.demo})


if not state.demo:

    @web_client.get("/config", response_class=HTMLResponse)
    def config_page(request: Request):
        return templates.TemplateResponse("config.html", context={"request": request})

    @web_client.get("/config/content_type/github", response_class=HTMLResponse)
    def github_config_page(request: Request):
        default_copy = constants.default_config.copy()
        default_github = default_copy["content-type"]["github"]  # type: ignore

        default_config = TextContentConfig(
            compressed_jsonl=default_github["compressed-jsonl"],
            embeddings_file=default_github["embeddings-file"],
        )

        current_config = (
            state.config.content_type.github
            if state.config and state.config.content_type and state.config.content_type.github
            else default_config
        )

        current_config = json.loads(current_config.json())

        return templates.TemplateResponse(
            "content_type_github_input.html", context={"request": request, "current_config": current_config}
        )

    @web_client.get("/config/content_type/{content_type}", response_class=HTMLResponse)
    def content_config_page(request: Request, content_type: str):
        if content_type not in VALID_CONTENT_TYPES:
            return templates.TemplateResponse("config.html", context={"request": request})

        default_copy = constants.default_config.copy()
        default_content_type = default_copy["content-type"][content_type]  # type: ignore

        default_config = TextContentConfig(
            compressed_jsonl=default_content_type["compressed-jsonl"],
            embeddings_file=default_content_type["embeddings-file"],
        )

        current_config = (
            state.config.content_type[content_type]
            if state.config and state.config.content_type and state.config.content_type[content_type]  # type: ignore
            else default_config
        )
        current_config = json.loads(current_config.json())

        return templates.TemplateResponse(
            "content_type_input.html",
            context={
                "request": request,
                "current_config": current_config,
                "content_type": content_type,
            },
        )

    @web_client.get("/config/processor/conversation", response_class=HTMLResponse)
    def conversation_processor_config_page(request: Request):
        default_copy = constants.default_config.copy()
        default_processor_config = default_copy["processor"]["conversation"]  # type: ignore
        default_processor_config = ConversationProcessorConfig(
            openai_api_key="",
            model=default_processor_config["model"],
            conversation_logfile=default_processor_config["conversation-logfile"],
            chat_model=default_processor_config["chat-model"],
        )

        current_processor_conversation_config = (
            state.config.processor.conversation
            if state.config and state.config.processor and state.config.processor.conversation
            else default_processor_config
        )
        current_processor_conversation_config = json.loads(current_processor_conversation_config.json())

        return templates.TemplateResponse(
            "processor_conversation_input.html",
            context={
                "request": request,
                "current_config": current_processor_conversation_config,
            },
        )
