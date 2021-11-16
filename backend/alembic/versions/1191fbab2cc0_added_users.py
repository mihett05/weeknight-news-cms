"""Added users

Revision ID: 1191fbab2cc0
Revises: 
Create Date: 2021-11-16 18:05:31.363260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1191fbab2cc0"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_full_name"), "users", ["full_name"], unique=False)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.drop_index("ix_user_email", table_name="user")
    op.drop_index("ix_user_full_name", table_name="user")
    op.drop_index("ix_user_id", table_name="user")
    op.drop_table("user")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("email", sa.VARCHAR(), nullable=False),
        sa.Column("full_name", sa.VARCHAR(), nullable=True),
        sa.Column("hashed_password", sa.VARCHAR(), nullable=False),
        sa.Column("is_active", sa.BOOLEAN(), nullable=False),
        sa.Column("is_superuser", sa.BOOLEAN(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_user_id", "user", ["id"], unique=False)
    op.create_index("ix_user_full_name", "user", ["full_name"], unique=False)
    op.create_index("ix_user_email", "user", ["email"], unique=False)
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_full_name"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###