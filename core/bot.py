from typing import Tuple, Any, Optional
from loguru import logger
from loader import config
from utils import EmailValidator, LinkExtractor
from models import OperationResult
from .api import DawnExtensionAPI


class EmailBot(DawnExtensionAPI):
    def __init__(self, account: Account):
        super().__init__(account)

    async def validate_email(self) -> OperationResult:
        # 处理邮箱验证流程
        try:
            # 校验邮箱是否有效
            result = await EmailValidator(
                self.account_data.imap_server if not config.redirect_settings.enabled else config.redirect_settings.imap_server,
                self.account_data.email if not config.redirect_settings.enabled else config.redirect_settings.email,
                self.account_data.password if not config.redirect_settings.enabled else config.redirect_settings.password
            ).validate(None if config.redirect_settings.enabled and not config.redirect_settings.use_proxy else self.account_data.proxy)

            if not result["status"]:
                logger.error(f"Account: {self.account_data.email} | Email is invalid: {result['data']}")
                return OperationResult(
                    identifier=self.account_data.email,
                    data=self.account_data.password,
                    status=False,
                )

            logger.info(f"Account: {self.account_data.email} | Email is valid")
            return OperationResult(
                identifier=self.account_data.email,
                data=self.account_data.password,
                status=True,
            )

        except Exception as error:
            logger.error(f"Account: {self.account_data.email} | Email validation failed: {error}")
            return OperationResult(
                identifier=self.account_data.email,
                data=self.account_data.password,
                status=False,
            )

    async def extract_confirmation_link(self) -> OperationResult:
        # 提取确认链接
        try:
            confirm_url = await LinkExtractor(
                mode="verify",
                imap_server=self.account_data.imap_server if not config.redirect_settings.enabled else config.redirect_settings.imap_server,
                email=self.account_data.email if not config.redirect_settings.enabled else config.redirect_settings.email,
                password=self.account_data.password if not config.redirect_settings.enabled else config.redirect_settings.password
            ).extract_link(None if config.redirect_settings.enabled and not config.redirect_settings.use_proxy else self.account_data.proxy)

            if not confirm_url["status"]:
                logger.error(f"Account: {self.account_data.email} | Confirmation link not found: {confirm_url['data']}")
                return OperationResult(
                    identifier=self.account_data.email,
                    data=self.account_data.password,
                    status=False,
                )

            logger.success(f"Account: {self.account_data.email} | Link found, proceeding with email confirmation")
            return OperationResult(
                identifier=self.account_data.email,
                data=confirm_url["data"],
                status=True,
            )

        except Exception as error:
            logger.error(f"Account: {self.account_data.email} | Failed to extract confirmation link: {error}")
            return OperationResult(
                identifier=self.account_data.email,
                data=self.account_data.password,
                status=False,
            )
