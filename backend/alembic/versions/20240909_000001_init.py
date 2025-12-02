from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20240909_000001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
	op.create_table(
		'users',
		sa.Column('id', sa.Integer(), primary_key=True),
		sa.Column('email', sa.String(length=254), nullable=False, unique=True),
		sa.Column('password_hash', sa.String(length=255), nullable=False),
		sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
	)
	op.create_index('ix_users_email', 'users', ['email'])

	op.create_table(
		'wishlists',
		sa.Column('id', sa.Integer(), primary_key=True),
		sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
		sa.Column('title', sa.String(length=100), nullable=False),
		sa.Column('description', sa.Text(), nullable=True),
		sa.Column('is_public', sa.Boolean(), nullable=False, server_default=sa.false()),
		sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
	)
	op.create_index('ix_wishlists_user_id', 'wishlists', ['user_id'])

	op.create_table(
		'gifts',
		sa.Column('id', sa.Integer(), primary_key=True),
		sa.Column('wishlist_id', sa.Integer(), sa.ForeignKey('wishlists.id', ondelete='CASCADE'), nullable=False),
		sa.Column('name', sa.String(length=100), nullable=False),
		sa.Column('price', sa.Numeric(12, 2), nullable=True),
		sa.Column('image_url', sa.Text(), nullable=True),
		sa.Column('purchase_link', sa.Text(), nullable=True),
		sa.Column('status', sa.String(length=20), nullable=False, server_default='Available'),
		sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
	)
	op.create_index('ix_gifts_wishlist_id', 'gifts', ['wishlist_id'])


def downgrade() -> None:
	op.drop_table('gifts')
	op.drop_table('wishlists')
	op.drop_table('users')


