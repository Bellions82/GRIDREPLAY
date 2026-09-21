from alembic import op
import sqlalchemy as sa

revision = "0002_generation_qa"
down_revision = "0001_initial"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "generation_records",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("project_id", sa.String(64), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("shot_id", sa.String(64), sa.ForeignKey("shots.id", ondelete="CASCADE"), nullable=False),
        sa.Column("job_id", sa.String(64), sa.ForeignKey("render_jobs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("provider", sa.String(128), nullable=False),
        sa.Column("model", sa.String(128), nullable=False),
        sa.Column("model_version", sa.String(128), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("negative_prompt", sa.Text(), nullable=False),
        sa.Column("seed", sa.Integer()),
        sa.Column("parameters", sa.JSON(), nullable=False),
        sa.Column("references", sa.JSON(), nullable=False),
        sa.Column("artifact_uri", sa.Text()),
        sa.Column("artifact_metadata", sa.JSON(), nullable=False),
        sa.Column("qc_result", sa.JSON()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("shot_id", "version", name="uq_generation_shot_version"),
    )
    op.create_index("ix_generation_records_project_id", "generation_records", ["project_id"])
    op.create_index("ix_generation_records_shot_id", "generation_records", ["shot_id"])
    op.create_index("ix_generation_records_job_id", "generation_records", ["job_id"])

    op.create_table(
        "qa_results",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("project_id", sa.String(64), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("shot_id", sa.String(64), sa.ForeignKey("shots.id", ondelete="CASCADE"), nullable=False),
        sa.Column("job_id", sa.String(64), sa.ForeignKey("render_jobs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("generation_id", sa.String(64), sa.ForeignKey("generation_records.id", ondelete="CASCADE"), nullable=False),
        sa.Column("attempt", sa.Integer(), nullable=False),
        sa.Column("technical", sa.String(16), nullable=False),
        sa.Column("visual", sa.String(16), nullable=False),
        sa.Column("character", sa.String(16), nullable=False),
        sa.Column("environment", sa.String(16), nullable=False),
        sa.Column("temporal", sa.String(16), nullable=False),
        sa.Column("timeline", sa.String(16), nullable=False),
        sa.Column("decision", sa.String(16), nullable=False),
        sa.Column("failure_codes", sa.JSON(), nullable=False),
        sa.Column("repair_plan", sa.JSON(), nullable=False),
        sa.Column("metrics", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_qa_results_project_id", "qa_results", ["project_id"])
    op.create_index("ix_qa_results_shot_id", "qa_results", ["shot_id"])
    op.create_index("ix_qa_results_job_id", "qa_results", ["job_id"])
    op.create_index("ix_qa_results_generation_id", "qa_results", ["generation_id"])
    op.create_index("ix_qa_results_decision", "qa_results", ["decision"])

def downgrade() -> None:
    op.drop_table("qa_results")
    op.drop_table("generation_records")
