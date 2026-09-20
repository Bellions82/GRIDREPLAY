from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table("projects", sa.Column("id", sa.String(64), primary_key=True), sa.Column("title", sa.String(200), nullable=False), sa.Column("schema_version", sa.String(20), nullable=False), sa.Column("status", sa.String(32), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("assets", sa.Column("id", sa.String(64), primary_key=True), sa.Column("project_id", sa.String(64), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False), sa.Column("kind", sa.String(32), nullable=False), sa.Column("uri", sa.Text(), nullable=False), sa.Column("version", sa.Integer(), nullable=False), sa.Column("metadata_json", sa.JSON(), nullable=False))
    op.create_index("ix_assets_project_id", "assets", ["project_id"])
    op.create_table("scenes", sa.Column("id", sa.String(64), primary_key=True), sa.Column("project_id", sa.String(64), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False), sa.Column("ordinal", sa.Integer(), nullable=False), sa.Column("title", sa.String(200), nullable=False), sa.Column("status", sa.String(32), nullable=False), sa.Column("data", sa.JSON(), nullable=False), sa.UniqueConstraint("project_id", "ordinal", name="uq_scene_project_ordinal"))
    op.create_index("ix_scenes_project_id", "scenes", ["project_id"])
    op.create_table("shots", sa.Column("id", sa.String(64), primary_key=True), sa.Column("scene_id", sa.String(64), sa.ForeignKey("scenes.id", ondelete="CASCADE"), nullable=False), sa.Column("ordinal", sa.Integer(), nullable=False), sa.Column("duration", sa.Float(), nullable=False), sa.Column("status", sa.String(32), nullable=False), sa.Column("data", sa.JSON(), nullable=False), sa.UniqueConstraint("scene_id", "ordinal", name="uq_shot_scene_ordinal"))
    op.create_index("ix_shots_scene_id", "shots", ["scene_id"])
    op.create_table("render_jobs", sa.Column("id", sa.String(64), primary_key=True), sa.Column("project_id", sa.String(64), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False), sa.Column("shot_id", sa.String(64), sa.ForeignKey("shots.id", ondelete="CASCADE"), nullable=False), sa.Column("fingerprint", sa.String(64), nullable=False, unique=True), sa.Column("state", sa.String(32), nullable=False), sa.Column("attempts", sa.Integer(), nullable=False), sa.Column("payload", sa.JSON(), nullable=False), sa.Column("lease_owner", sa.String(128)), sa.Column("lease_expires_at", sa.DateTime(timezone=True)), sa.Column("heartbeat_at", sa.DateTime(timezone=True)), sa.Column("last_error", sa.Text()), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_render_jobs_project_id", "render_jobs", ["project_id"])
    op.create_index("ix_render_jobs_shot_id", "render_jobs", ["shot_id"])
    op.create_index("ix_render_jobs_fingerprint", "render_jobs", ["fingerprint"])
    op.create_index("ix_render_jobs_state", "render_jobs", ["state"])

def downgrade() -> None:
    op.drop_table("render_jobs")
    op.drop_table("shots")
    op.drop_table("scenes")
    op.drop_table("assets")
    op.drop_table("projects")
