"""empty message

Revision ID: 848081ed9b59
Revises:
Create Date: 2020-05-17 14:50:42.166683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '848081ed9b59'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=True))

    op.execute('UPDATE todos SET completed = False WHERE completed IS NULL;')

    op.alter_column('todos', 'completed', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'completed')
    # ### end Alembic commands ###
