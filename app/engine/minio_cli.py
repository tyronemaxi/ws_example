#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: minio_cli.py
Time: 2024/1/10 3:33 PM
"""
from typing import BinaryIO
from io import BytesIO
from minio.helpers import MIN_PART_SIZE

from minio import Minio
from minio.error import S3Error
from app.common.log import logger
from conf.settings import MINIO_IP, MINIO_AK, MINIO_SK


class MinioCli(object):
    """
    API cli refers: https://min.io/docs/minio/linux/developers/python/API.html
    """
    def __init__(self, endpoint: str, access_key: str, secret_key: str):
        self.minio = Minio(endpoint=endpoint, access_key=access_key, secret_key=secret_key, secure=False)

    def get_minio_cli(self):
        """
        返回 minio cli obj
        :return:
        """
        return self.minio

    def create_bucket(self, bucket_name: str):
        """
        创建 bucket
        refers: https://min.io/docs/minio/linux/developers/python/API.html#make_bucket
        :param bucket_name 桶
        :return:
        """
        try:
            if not self.minio.bucket_exists(bucket_name):
                self.minio.make_bucket(bucket_name=bucket_name)

        except Exception as e:
            logger.error(f"[Minio] create bucket: {bucket_name} error for {e}")
            raise e

    def list_buckets(self):
        """
        列出 桶
        refers: https://min.io/docs/minio/linux/developers/python/API.html#list_buckets
        :return:
        """
        buckets = []
        try:
            buckets = self.minio.list_buckets()

        except Exception as e:
            logger.error(f"[Minio] list bucket error for {e}")
            raise e

        return buckets

    def fput_object(self, bucket_name: str, object_name: str, file_name: str):
        """
        创建文件对象
        refers: https://min.io/docs/minio/linux/developers/python/API.html#fput_object
        :return:
        """
        try:
            result = self.minio.fput_object(bucket_name, object_name, file_name)
            logger.info(f"[Minio] created {result.object_name}; etag: {result.etag}, version-id: {result.version_id}")

        except Exception as e:
            logger.error(f"[Minio] fput object, bucket_name: {bucket_name}, object_name: {object_name}, file_name: {file_name}")
            raise e

    def put_object(self, bucket_name: str, object_name: str, data: BinaryIO, length: int):
        """
        创建文件对象 - 数据
        refers: https://min.io/docs/minio/linux/developers/python/API.html#put_object
        param data - An object having callable read() returning bytes object.
        param length - Data size; -1 for unknown size and set valid part_size.
        :return:
        """
        try:
            if length == -1:
                # 未知文件大小，分块传输
                result = self.minio.put_object(bucket_name, object_name, data, length, part_size=MIN_PART_SIZE)
            else:
                result = self.minio.put_object(bucket_name, object_name, data, length)

            logger.info(f"[Minio] created {result.object_name}; etag: {result.etag}, version-id: {result.version_id}")

        except Exception as e:
            logger.error(f"[Minio] put object, bucket_name: {bucket_name}, object_name: {object_name}")
            raise e

    def check_object_exists(self, bucket_name: str, object_name: str):
        try:
            self.minio.stat_object(bucket_name, object_name)
            return True
        except S3Error as err:
            if err.code == 'NoSuchKey':
                return False
            else:
                return False

    def get_bytesio_object(self, bucket_name: str, obj_name: str):
        """
        从 minio 获取文档
        :param bucket_name: 桶
        :param obj_name: 对象名称
        :return:
        """
        try:
            resp = self.minio.get_object(bucket_name=bucket_name, object_name=obj_name)

            file_obj = BytesIO()
            file_obj.write(resp.read())
            file_obj.seek(0)

            return file_obj

        except Exception as e:
            raise e

    def remove_object(self, bucket_name: str, obj_name: str):
        """
        删除单个 object file
        refes: https://min.io/docs/minio/linux/developers/python/API.html#remove_object
        :param bucket_name: 桶
        :param obj_name: 对象名
        :return:
        """
        try:
            # 调用 remove_object 方法删除文件
            self.minio.remove_object(bucket_name, obj_name)
        except Exception as e:
            logger.error(f"[Minio] delete object, bucket_name: {bucket_name}, object_name: {obj_name}")
            raise e

    def upload_file_by_part(self, bucket_name: str, obj_name: str, file_path: str, part_size: int = 1024 * 1024 * 1024):
        """
        分块上传
        :param bucket_name:
        :param obj_name:
        :return:
        """
        try:
            # 分块上传文件
            self.minio.fput_object(
                bucket_name,
                obj_name,
                file_path,
                part_size=part_size
            )

        except Exception as e:
            logger.error(f"[Minio] delete object, bucket_name: {bucket_name}, object_name: {obj_name}")
            raise e


minio_cli = MinioCli(endpoint=MINIO_IP, access_key=MINIO_AK, secret_key=MINIO_SK)


def get_minio_cli():
    """
    获取 minio 原生客户端
    :return:
    """
    return minio_cli.get_minio_cli()


# if __name__ == '__main__':
    # # minio_cli.list_buckets()
    # bkts = minio_cli.list_buckets()
    # minio_cli.create_bucket('private-fin')
    # print(bkts)