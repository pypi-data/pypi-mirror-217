from pydantic import BaseModel, Field


class TemplateParams(BaseModel):
    update_template: str = Field(..., description="Template for update statement.")
    set_template: str = Field(..., description="Template for set statement.")
    where_template: str = Field(..., description="Template for where statement.")
    redact_template: str = Field(..., description="Template for redact statement.")
    replace_template: str = Field(..., description="Template for replace statement.")
    mask_template: str = Field(..., description="Template for mask statement.")
