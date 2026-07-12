import os
import time

import requests
from loguru import logger
from dotenv import load_dotenv

load_dotenv(".env")
modo = os.getenv("EXECUTION_MODE", "local")

LANDING_PATH = "./data/landing" if modo == "local" else "/landing"

print(f"Modo de execução: {modo}")


class DownloadTse:
    """
    Classe para download dos arquivos do TSE para o S3.

    """

    def __init__(self) -> None:
        pass

    def download_file(
        self,
        nome_file: str,
        url: str,
        max_tentativas: int = 3,
        ano: int | None = None,
        output_dir: str | None = "./data",
    ) -> dict | None:
        """
        Função responsavel por baixar os arquivos

        nome_file: nome do arquivo zip
        url: url de download
        max_tentativas: numero maximo de tentativas
        ano: ano da base para download
        output_dir: diretorio de saida para salvar o arquivo baixado, se None, retorna o arquivo em memória.
        """

        for tentativa in range(1, max_tentativas + 1):
            try:

                arquivo_downloaded = (
                    f"{nome_file}_{ano}.zip" if ano is not None else f"{nome_file}.zip"
                )

                if output_dir is None:
                    output_dir = None if modo == "lambda" else LANDING_PATH

                response = requests.get(url=url, timeout=60)

                response.raise_for_status()

                if modo != "lambda":
                    with open(arquivo_downloaded, "wb") as f:
                        f.write(response.content)

                return {"filename": arquivo_downloaded, "content": response.content}

            except requests.exceptions.Timeout:
                logger.debug(
                    f"Timeout na tentativa: {tentativa}, aguardando para executar novamente"
                )

            except Exception as e:
                logger.error(f"Erro ao baixar arquivo {arquivo_downloaded} : {e}")

            if tentativa < max_tentativas:
                time.sleep(2)

    def download_votacao_candidato_municipio(self, ano: int, path: str = None):
        """
        Votação nominal por município e zona
        """

        base_url: str = (
            "https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/votacao_candidato_munzona_{}.zip"
        )

        url = base_url.format(ano)

        logger.debug(f"baixando arquivos candidato_munzona_{ano}")

        if path is None:
            return self.download_file(
                ano=ano, nome_file="votacao_candidato_munzona", url=url
            )

        return self.download_file(
            ano=ano, nome_file=f"{path}/votacao_candidato_munzona", url=url
        )

    def download_municipios_ibge(self, path: str = None):
        """
        Dados do ibge
        """

        url: str = (
            "https://cdn.tse.jus.br/estatistica/sead/odsele/municipio_tse_ibge/municipio_tse_ibge.zip"
        )

        logger.debug("Baixando base de municipios....")

        if path is None:
            return self.download_file(nome_file="municipio_tse_ibge", url=url)

        return self.download_file(nome_file=f"{path}/municipio_tse_ibge", url=url)

    def download_vagas_disponiveis(self, ano: int, path: str = None):
        """
        Dados Vagas disponiveis
        """
        base_url: str = (
            "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_vagas/consulta_vagas_{}.zip"
        )

        url = base_url.format(ano)

        logger.debug(f"baixando arquivos de vagas_{ano}")

        if path is None:
            return self.download_file(ano=ano, nome_file="vagas", url=url)

        return self.download_file(ano=ano, nome_file=f"{path}/vagas", url=url)

    def download_coligacao(self, ano: int, path: str = None):
        """
        Dados de Coligação
        """
        base_url: str = (
            "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_coligacao/consulta_coligacao_{}.zip"
        )

        url = base_url.format(ano)

        logger.debug(f"baixando arquivos de coligacao_{ano}")

        if path is None:
            return self.download_file(ano=ano, nome_file="coligacao", url=url)

        return self.download_file(ano=ano, nome_file=f"{path}/coligacao", url=url)

    def download_info_complementares(self, ano: int, path: str = None):
        """
        Informações Complementares dos candidatos
        """
        base_url: str = (
            "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand_complementar/consulta_cand_complementar_{}.zip"
        )

        url = base_url.format(ano)

        if path is None:
            return self.download_file(
                ano=ano, nome_file="consulta_cand_complementar", url=url
            )

        logger.debug(f"baixando arquivos info_complementar_{ano}")

        if path is None:
            return self.download_file(
                ano=ano, nome_file="consulta_cand_complementar", url=url
            )

        return self.download_file(
            ano=ano, nome_file=f"{path}/consulta_cand_complementar", url=url
        )

    def download_bens_candidatos(self, ano: int, path: str = None):
        """
        Bens declarados pelos candidatos
        """
        base_url: str = (
            "https://cdn.tse.jus.br/estatistica/sead/odsele/bem_candidato/bem_candidato_{}.zip"
        )

        url = base_url.format(ano)

        logger.debug(f"baixando arquivos bem_candidato_{ano}")

        if path is None:
            return self.download_file(ano=ano, nome_file="bem_candidato", url=url)

        return self.download_file(ano=ano, nome_file=f"{path}/bem_candidato", url=url)

    def download_candidatos(self, ano: int, path: str = None):
        """
        Candidatos
        """
        base_url: str = (
            "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_{}.zip"
        )

        url = base_url.format(ano)

        logger.debug(f"baixando arquivos de candidatos_{ano}")

        if path is None:
            return self.download_file(ano=ano, nome_file="consulta_cand", url=url)

        return self.download_file(ano=ano, nome_file=f"{path}/consulta_cand", url=url)

    def download_ano(self, anos: list) -> list[dict] | None:
        """
        Download de dados as bases
        """

        arquivos = []

        if modo == "lambda":
            logger.info("Executando em modo lambda, baixando arquivos para memória")

            for ano in anos:
                logger.info(f"Baixando dados do TSE para os anos: {ano}")

                arquivos.append(self.download_bens_candidatos(ano=ano, path=None))

                arquivos.append(
                    self.download_votacao_candidato_municipio(ano=ano, path=None)
                )

                arquivos.append(self.download_municipios_ibge(path=None))

                arquivos.append(self.download_vagas_disponiveis(ano=ano, path=None))

                arquivos.append(self.download_coligacao(ano=ano, path=None))

                arquivos.append(self.download_info_complementares(ano=ano, path=None))

                arquivos.append(self.download_candidatos(ano=ano, path=None))

            return arquivos

        if modo == "local":
            logger.info("Executando em modo local, baixando arquivos para disco")
            for ano in anos:
                logger.info(f"Baixando dados do TSE para os anos: {ano}")
                if not os.path.exists(os.path.join(LANDING_PATH, str(ano))):
                    os.makedirs(os.path.join(LANDING_PATH, str(ano)))

                arquivos.append(
                    self.download_bens_candidatos(
                        ano=ano, path=os.path.join(LANDING_PATH, str(ano))
                    )
                )

                arquivos.append(
                    self.download_votacao_candidato_municipio(
                        ano=ano, path=os.path.join(LANDING_PATH, str(ano))
                    )
                )

                arquivos.append(
                    self.download_municipios_ibge(
                        path=os.path.join(LANDING_PATH, str(ano))
                    )
                )
                arquivos.append(
                    self.download_vagas_disponiveis(
                        ano=ano, path=os.path.join(LANDING_PATH, str(ano))
                    )
                )
                arquivos.append(
                    self.download_coligacao(
                        ano=ano, path=os.path.join(LANDING_PATH, str(ano))
                    )
                )
                arquivos.append(
                    self.download_info_complementares(
                        ano=ano, path=os.path.join(LANDING_PATH, str(ano))
                    )
                )
                arquivos.append(
                    self.download_candidatos(
                        ano=ano, path=os.path.join(LANDING_PATH, str(ano))
                    )
                )
