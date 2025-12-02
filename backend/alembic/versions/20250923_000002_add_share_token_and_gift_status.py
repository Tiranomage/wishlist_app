from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250923_000002'
down_revision = '20240909_000001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add share_token column to wishlists
    op.add_column('wishlists', sa.Column('share_token', sa.String(length=5), nullable=True))
    op.create_unique_constraint('uq_wishlists_share_token', 'wishlists', ['share_token'])
    op.create_index('ix_wishlists_share_token', 'wishlists', ['share_token'], unique=False)
    # Ensure gifts.status column exists and set default to 'Свободен'
    try:
        op.alter_column('gifts', 'status', existing_type=sa.String(length=32), nullable=False, server_default='Свободен')
    except Exception:
        # Column may already exist with correct settings; ignore
        pass


def downgrade() -> None:
    try:
        op.drop_index('ix_wishlists_share_token', table_name='wishlists')
    except Exception:
        pass
    try:
        op.drop_constraint('uq_wishlists_share_token', 'wishlists', type_='unique')
    except Exception:
        pass
    with op.batch_alter_table('wishlists') as batch_op:
        try:
            batch_op.drop_column('share_token')
        except Exception:
            pass

