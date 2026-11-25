"""create analysis result tables"""
from alembic import op
import sqlalchemy as sa

revision = "003_create_analyses"
down_revision = "002_create_cv_and_jobs"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("analyses", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("cv_id", sa.Integer(), sa.ForeignKey("cvs.id", ondelete="CASCADE"), nullable=False), sa.Column("job_offer_id", sa.Integer(), sa.ForeignKey("job_offers.id", ondelete="CASCADE"), nullable=False), sa.Column("score", sa.Float(), nullable=False), sa.Column("skills_score", sa.Float(), nullable=False), sa.Column("experience_score", sa.Float(), nullable=False), sa.Column("education_score", sa.Float(), nullable=False), sa.Column("keywords_score", sa.Float(), nullable=False), sa.Column("explanation", sa.Text(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_index("ix_analyses_user_id", "analyses", ["user_id"])
    op.create_table("match_details", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("analysis_id", sa.Integer(), sa.ForeignKey("analyses.id", ondelete="CASCADE"), nullable=False), sa.Column("skill", sa.String(120), nullable=False), sa.Column("matched", sa.Boolean(), nullable=False))
    op.create_index("ix_match_details_analysis_id", "match_details", ["analysis_id"])
    op.create_table("recommendations", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("analysis_id", sa.Integer(), sa.ForeignKey("analyses.id", ondelete="CASCADE"), nullable=False), sa.Column("text", sa.Text(), nullable=False))
    op.create_index("ix_recommendations_analysis_id", "recommendations", ["analysis_id"])


def downgrade() -> None:
    op.drop_table("recommendations")
    op.drop_table("match_details")
    op.drop_table("analyses")

