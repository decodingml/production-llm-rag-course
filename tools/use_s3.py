import click

from second_brain.infrastructure.aws.s3 import S3Client


@click.group()
def cli() -> None:
    """CLI tool for uploading and downloading folders to/from S3."""
    pass


@cli.command()
@click.argument("local_path")
@click.argument("bucket_name")
@click.option("--s3-prefix", default="", help="Optional S3 prefix (folder path)")
def upload(local_path: str, bucket_name: str, s3_prefix: str) -> None:
    """Upload a local folder to S3 bucket.

    Args:
        local_path: Path to the local folder to upload
        bucket_name: Name of the S3 bucket
        s3_prefix: Optional S3 prefix (folder path)

    Raises:
        click.Abort: If upload fails or path is invalid
    """
    try:
        s3_client = S3Client(bucket_name)
        s3_client.upload_folder(local_path, s3_prefix)
        click.echo(
            f"Successfully uploaded {local_path} to s3://{bucket_name}/{s3_prefix}"
        )
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


@cli.command()
@click.argument("bucket_name")
@click.argument("s3_path")
@click.argument("local_path")
def download(bucket_name: str, s3_path: str, local_path: str) -> None:
    """Download a zipped folder from S3 and extract it to local storage.

    Args:
        bucket_name: Name of the S3 bucket
        s3_path: Path to the zip file in S3 bucket
        local_path: Local path where files should be extracted

    Raises:
        click.Abort: If download fails or path is invalid
    """

    try:
        s3_client = S3Client(bucket_name)
        s3_client.download_folder(s3_path, local_path)
        click.echo(
            f"Successfully downloaded s3://{bucket_name}/{s3_path} to {local_path}"
        )
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    cli()
