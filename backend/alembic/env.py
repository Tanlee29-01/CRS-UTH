import sys
import os
from logging.config import fileConfig

# --- BẮT ĐẦU PHẦN MÃ THÊM MỚI ---
# Tìm đường dẫn tuyệt đối của thư mục chứa file env.py hiện tại (thư mục alembic)
# Sau đó lùi ra ngoài 1 cấp để lấy đường dẫn của thư mục 'backend'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Đưa thư mục 'backend' vào đầu danh sách tìm kiếm thư viện của Python
sys.path.insert(0, BASE_DIR)
# --- KẾT THÚC PHẦN MÃ THÊM MỚI ---

from alembic import context
from sqlalchemy import engine_from_config, pool

# Bây giờ Python đã có thể tìm thấy thư mục 'app' một cách dễ dàng!
from app.core.config import settings
from app.db.base import Base
from app import models  # noqa: F401

config = context.config
config.set_main_option("sqlalchemy.url", settings.get_database_url())

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
