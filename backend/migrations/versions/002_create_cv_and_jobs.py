"""create cv and job offer tables"""
from alembic import op
import sqlalchemy as sa

revision = "002_create_cv_and_jobs"
down_revision = "001_create_users"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("cvs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("filename", sa.String(255), nullable=False), sa.Column("storage_path", sa.String(500), nullable=False), sa.Column("extracted_text", sa.Text(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_index("ix_cvs_user_id", "cvs", ["user_id"])
    op.create_unique_constraint("uq_cvs_storage_path", "cvs", ["storage_path"])
    op.create_table("job_offers", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("title", sa.String(200), nullable=False), sa.Column("company", sa.String(200)), sa.Column("description", sa.Text(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_index("ix_job_offers_user_id", "job_offers", ["user_id"])


def downgrade() -> None:
    op.drop_table("job_offers")
    op.drop_constraint("uq_cvs_storage_path", "cvs", type_="unique")
    op.drop_table("cvs")

