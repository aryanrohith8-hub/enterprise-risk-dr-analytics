import sys
import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns
import sqlalchemy


def main():

    print("=" * 60)
    print("ENTERPRISE RISK & DISASTER RECOVERY ANALYTICS PLATFORM")
    print("=" * 60)

    print("\nPROJECT ENVIRONMENT")
    print("-------------------")

    print("Python Version:", sys.version.split()[0])
    print("Pandas Version:", pd.__version__)
    print("NumPy Version:", np.__version__)
    print("Matplotlib Version:", matplotlib.__version__)
    print("Seaborn Version:", sns.__version__)
    print("SQLAlchemy Version:", sqlalchemy.__version__)

    print("\nProject environment is ready!")


if __name__ == "__main__":
    main()