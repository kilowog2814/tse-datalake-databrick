import zipfile

from src.shared import Shared
from pathlib import Path

shared = Shared()

landing_root = Path(shared.data_path) / shared.landing_path
bronze_root = Path(shared.data_path) / shared.bronze_path

Path(bronze_root).mkdir(parents=True, exist_ok=True)


class UnzipFiles:
    """
    Classe para descompactar arquivos ZIP.
    """

    def __init__(self):
        pass

    def unzip_file(self, zip_file_path: str, output_dir: str) -> None:
        """
        Descompacta um arquivo ZIP para o diretório de saída especificado.

        Args:
            zip_file_path (str): Caminho do arquivo ZIP a ser descompactado.
            output_dir (str): Diretório onde os arquivos descompactados serão salvos.
        """

        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(output_dir)

    def unzip_files_in_directory(self) -> None:
        """
        Descompacta todos os arquivos ZIP em um diretório especificado.

        """

        pasta = Path(landing_root)

        arquivos_zip = list(pasta.rglob("*.zip"))
        shared.logger.info(f"Arquivos ZIP encontrados: {len(arquivos_zip)}")

        if not arquivos_zip:
            shared.logger.warning("Nenhum arquivo ZIP encontrado.")
            return

        for arquivo in arquivos_zip:
            output_dir = arquivo.parent / arquivo.stem

            output_dir = str(output_dir).replace(
                shared.landing_path, shared.bronze_path
            )
            Path(output_dir).mkdir(parents=True, exist_ok=True)

            shared.logger.info(f"Descompactando arquivo: {arquivo}")
            self.unzip_file(str(arquivo), output_dir)


utils = UnzipFiles()

utils.unzip_files_in_directory()
