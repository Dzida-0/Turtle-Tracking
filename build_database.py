from lambda_function.download_function.lambda_function import lambda_handler as download_data
from lambda_function.save_function.lambda_function import lambda_handler as save_data
if __name__ == '__main__':
    download_data(None,None)
    save_data(None,None)