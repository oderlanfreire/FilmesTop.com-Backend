"""adição das colunas nota final_final e total_avaliacoes a tabela Filmes

Revision ID: d91613a242a0
Revises: d73520a17a53
Create Date: 2024-09-15 12:52:39.158595

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd91613a242a0'
down_revision: Union[str, None] = 'd73520a17a53'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('filmes', sa.Column('nota_final', sa.Numeric(precision=2, scale=1), nullable=True))
    op.add_column('filmes', sa.Column('total_avaliacoes', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('filmes', 'total_avaliacoes')
    op.drop_column('filmes', 'nota_final')
    # ### end Alembic commands ###
