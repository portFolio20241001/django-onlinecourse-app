#!/usr/bin/env python
"""Django の管理タスクを実行するためのコマンドラインユーティリティ"""

import os  # OS関連の機能を提供するモジュールをインポート
import sys  # システム関連の機能を提供するモジュールをインポート


def main():
    """Django の管理タスクを実行するメイン関数"""
    # Django の設定モジュールを環境変数に設定（'myproject.settings' を指定）
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

    try:
        # Django の管理コマンドを実行する関数をインポート
        from django.core.management import execute_from_command_line
    except ImportError as exc:  # Django がインポートできなかった場合のエラーハンドリング
        raise ImportError(
            "Django をインポートできませんでした。Django がインストールされていて、"
            "PYTHONPATH 環境変数で正しく参照されていることを確認してください。"
            "仮想環境の有効化を忘れていませんか？"
        ) from exc  # エラーメッセージを出力し、元の例外情報を保持

    # コマンドライン引数を Django の管理コマンドに渡して実行
    execute_from_command_line(sys.argv)


# スクリプトが直接実行された場合に main() を呼び出す
if __name__ == '__main__':
    main()
