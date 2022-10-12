{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "CDD-ML-Part-2-Exploratory-Data-Analysis.ipynb",
      "provenance": [],
      "collapsed_sections": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "metadata": {
        "id": "H0mjQ2PcrSe5"
      },
      "source": [
        "! wget https://repo.anaconda.com/miniconda/Miniconda3-py37_4.8.2-Linux-x86_64.sh\n",
        "! chmod +x Miniconda3-py37_4.8.2-Linux-x86_64.sh\n",
        "! bash ./Miniconda3-py37_4.8.2-Linux-x86_64.sh -b -f -p /usr/local\n",
        "! conda install -c rdkit rdkit -y\n",
        "import sys\n",
        "sys.path.append('/usr/local/lib/python3.7/site-packages/')"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Fpu5C7HlwV9s"
      },
      "source": [
        "import pandas as pd"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "GCcE8J5XwjtB"
      },
      "source": [
        "df = pd.read_csv('bioactivity_data_preprocessed.csv')"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "9qn_eQcnxY7C"
      },
      "source": [
        "### **Import libraries**"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "CgBjIdT-rnRU"
      },
      "source": [
        "import numpy as np\n",
        "from rdkit import Chem\n",
        "from rdkit.Chem import Descriptors, Lipinski"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "JsgTV-ByxdMa"
      },
      "source": [
        "### **Calculate descriptors**"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "bCXEY7a9ugO_"
      },
      "source": [
        "# Inspired by: https://codeocean.com/explore/capsules?query=tag:data-curation\n",
        "\n",
        "def lipinski(smiles, verbose=False):\n",
        "\n",
        "    moldata= []\n",
        "    for elem in smiles:\n",
        "        mol=Chem.MolFromSmiles(elem) \n",
        "        moldata.append(mol)\n",
        "       \n",
        "    baseData= np.arange(1,1)\n",
        "    i=0  \n",
        "    for mol in moldata:        \n",
        "       \n",
        "        desc_MolWt = Descriptors.MolWt(mol)\n",
        "        desc_MolLogP = Descriptors.MolLogP(mol)\n",
        "        desc_NumHDonors = Lipinski.NumHDonors(mol)\n",
        "        desc_NumHAcceptors = Lipinski.NumHAcceptors(mol)\n",
        "           \n",
        "        row = np.array([desc_MolWt,\n",
        "                        desc_MolLogP,\n",
        "                        desc_NumHDonors,\n",
        "                        desc_NumHAcceptors])   \n",
        "    \n",
        "        if(i==0):\n",
        "            baseData=row\n",
        "        else:\n",
        "            baseData=np.vstack([baseData, row])\n",
        "        i=i+1      \n",
        "    \n",
        "    columnNames=[\"MW\",\"LogP\",\"NumHDonors\",\"NumHAcceptors\"]   \n",
        "    descriptors = pd.DataFrame(data=baseData,columns=columnNames)\n",
        "    \n",
        "    return descriptors"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "ThFIFw8IukMY"
      },
      "source": [
        "df_lipinski = lipinski(df.canonical_smiles)"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "gUMlPfFrxicj"
      },
      "source": [
        "### **Combine DataFrames**\n",
        "\n",
        "Let's take a look at the 2 DataFrames that will be combined."
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "DaezyM5vwp9n",
        "outputId": "fb750119-b086-4d9d-e9f7-190833e4dc74",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 415
        }
      },
      "source": [
        "df_lipinski"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>MW</th>\n",
              "      <th>LogP</th>\n",
              "      <th>NumHDonors</th>\n",
              "      <th>NumHAcceptors</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>281.271</td>\n",
              "      <td>1.89262</td>\n",
              "      <td>0.0</td>\n",
              "      <td>5.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>415.589</td>\n",
              "      <td>3.81320</td>\n",
              "      <td>0.0</td>\n",
              "      <td>2.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>421.190</td>\n",
              "      <td>2.66050</td>\n",
              "      <td>0.0</td>\n",
              "      <td>4.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>293.347</td>\n",
              "      <td>3.63080</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>338.344</td>\n",
              "      <td>3.53900</td>\n",
              "      <td>0.0</td>\n",
              "      <td>5.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>...</th>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>128</th>\n",
              "      <td>338.359</td>\n",
              "      <td>3.40102</td>\n",
              "      <td>0.0</td>\n",
              "      <td>5.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>129</th>\n",
              "      <td>296.366</td>\n",
              "      <td>3.44330</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>130</th>\n",
              "      <td>276.291</td>\n",
              "      <td>4.09564</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>131</th>\n",
              "      <td>278.307</td>\n",
              "      <td>3.29102</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>132</th>\n",
              "      <td>282.383</td>\n",
              "      <td>4.10530</td>\n",
              "      <td>0.0</td>\n",
              "      <td>2.0</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>133 rows × 4 columns</p>\n",
              "</div>"
            ],
            "text/plain": [
              "          MW     LogP  NumHDonors  NumHAcceptors\n",
              "0    281.271  1.89262         0.0            5.0\n",
              "1    415.589  3.81320         0.0            2.0\n",
              "2    421.190  2.66050         0.0            4.0\n",
              "3    293.347  3.63080         0.0            3.0\n",
              "4    338.344  3.53900         0.0            5.0\n",
              "..       ...      ...         ...            ...\n",
              "128  338.359  3.40102         0.0            5.0\n",
              "129  296.366  3.44330         0.0            3.0\n",
              "130  276.291  4.09564         0.0            3.0\n",
              "131  278.307  3.29102         0.0            3.0\n",
              "132  282.383  4.10530         0.0            2.0\n",
              "\n",
              "[133 rows x 4 columns]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 7
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "9-ChzM8_wuq_",
        "outputId": "5f5be1ae-c757-44af-cace-5a4c083a81af",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 415
        }
      },
      "source": [
        "df"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>molecule_chembl_id</th>\n",
              "      <th>canonical_smiles</th>\n",
              "      <th>standard_value</th>\n",
              "      <th>bioactivity_class</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>CHEMBL187579</td>\n",
              "      <td>Cc1noc(C)c1CN1C(=O)C(=O)c2cc(C#N)ccc21</td>\n",
              "      <td>7200.0</td>\n",
              "      <td>intermediate</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>CHEMBL188487</td>\n",
              "      <td>O=C1C(=O)N(Cc2ccc(F)cc2Cl)c2ccc(I)cc21</td>\n",
              "      <td>9400.0</td>\n",
              "      <td>intermediate</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>CHEMBL185698</td>\n",
              "      <td>O=C1C(=O)N(CC2COc3ccccc3O2)c2ccc(I)cc21</td>\n",
              "      <td>13500.0</td>\n",
              "      <td>inactive</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>CHEMBL426082</td>\n",
              "      <td>O=C1C(=O)N(Cc2cc3ccccc3s2)c2ccccc21</td>\n",
              "      <td>13110.0</td>\n",
              "      <td>inactive</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>CHEMBL187717</td>\n",
              "      <td>O=C1C(=O)N(Cc2cc3ccccc3s2)c2c1cccc2[N+](=O)[O-]</td>\n",
              "      <td>2000.0</td>\n",
              "      <td>intermediate</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>...</th>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>128</th>\n",
              "      <td>CHEMBL2146517</td>\n",
              "      <td>COC(=O)[C@@]1(C)CCCc2c1ccc1c2C(=O)C(=O)c2c(C)c...</td>\n",
              "      <td>10600.0</td>\n",
              "      <td>inactive</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>129</th>\n",
              "      <td>CHEMBL187460</td>\n",
              "      <td>C[C@H]1COC2=C1C(=O)C(=O)c1c2ccc2c1CCCC2(C)C</td>\n",
              "      <td>10100.0</td>\n",
              "      <td>inactive</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>130</th>\n",
              "      <td>CHEMBL363535</td>\n",
              "      <td>Cc1coc2c1C(=O)C(=O)c1c-2ccc2c(C)cccc12</td>\n",
              "      <td>11500.0</td>\n",
              "      <td>inactive</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>131</th>\n",
              "      <td>CHEMBL227075</td>\n",
              "      <td>Cc1cccc2c3c(ccc12)C1=C(C(=O)C3=O)[C@@H](C)CO1</td>\n",
              "      <td>10700.0</td>\n",
              "      <td>inactive</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>132</th>\n",
              "      <td>CHEMBL45830</td>\n",
              "      <td>CC(C)C1=Cc2ccc3c(c2C(=O)C1=O)CCCC3(C)C</td>\n",
              "      <td>78900.0</td>\n",
              "      <td>inactive</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>133 rows × 4 columns</p>\n",
              "</div>"
            ],
            "text/plain": [
              "    molecule_chembl_id  ... bioactivity_class\n",
              "0         CHEMBL187579  ...      intermediate\n",
              "1         CHEMBL188487  ...      intermediate\n",
              "2         CHEMBL185698  ...          inactive\n",
              "3         CHEMBL426082  ...          inactive\n",
              "4         CHEMBL187717  ...      intermediate\n",
              "..                 ...  ...               ...\n",
              "128      CHEMBL2146517  ...          inactive\n",
              "129       CHEMBL187460  ...          inactive\n",
              "130       CHEMBL363535  ...          inactive\n",
              "131       CHEMBL227075  ...          inactive\n",
              "132        CHEMBL45830  ...          inactive\n",
              "\n",
              "[133 rows x 4 columns]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 8
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "eET6iZ1Aw3oe"
      },
      "source": [
        "Now, let's combine the 2 DataFrame"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "L9nUZC0Ww3gp"
      },
      "source": [
        "df_combined = pd.concat([df,df_lipinski], axis=1)"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "FRBfBP3QxFJp",
        "outputId": "18e69e90-6b93-4b8f-fc86-24924f6eb00c",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 487
        }
      },
      "source": [
        "df_combined"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>molecule_chembl_id</th>\n",
              "      <th>canonical_smiles</th>\n",
              "      <th>standard_value</th>\n",
              "      <th>bioactivity_class</th>\n",
              "      <th>MW</th>\n",
              "      <th>LogP</th>\n",
              "      <th>NumHDonors</th>\n",
              "      <th>NumHAcceptors</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>CHEMBL187579</td>\n",
              "      <td>Cc1noc(C)c1CN1C(=O)C(=O)c2cc(C#N)ccc21</td>\n",
              "      <td>7200.0</td>\n",
              "      <td>intermediate</td>\n",
              "      <td>281.271</td>\n",
              "      <td>1.89262</td>\n",
              "      <td>0.0</td>\n",
              "      <td>5.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>CHEMBL188487</td>\n",
              "      <td>O=C1C(=O)N(Cc2ccc(F)cc2Cl)c2ccc(I)cc21</td>\n",
              "      <td>9400.0</td>\n",
              "      <td>intermediate</td>\n",
              "      <td>415.589</td>\n",
              "      <td>3.81320</td>\n",
              "      <td>0.0</td>\n",
              "      <td>2.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>CHEMBL185698</td>\n",
              "      <td>O=C1C(=O)N(CC2COc3ccccc3O2)c2ccc(I)cc21</td>\n",
              "      <td>13500.0</td>\n",
              "      <td>inactive</td>\n",
              "      <td>421.190</td>\n",
              "      <td>2.66050</td>\n",
              "      <td>0.0</td>\n",
              "      <td>4.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>CHEMBL426082</td>\n",
              "      <td>O=C1C(=O)N(Cc2cc3ccccc3s2)c2ccccc21</td>\n",
              "      <td>13110.0</td>\n",
              "      <td>inactive</td>\n",
              "      <td>293.347</td>\n",
              "      <td>3.63080</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>CHEMBL187717</td>\n",
              "      <td>O=C1C(=O)N(Cc2cc3ccccc3s2)c2c1cccc2[N+](=O)[O-]</td>\n",
              "      <td>2000.0</td>\n",
              "      <td>intermediate</td>\n",
              "      <td>338.344</td>\n",
              "      <td>3.53900</td>\n",
              "      <td>0.0</td>\n",
              "      <td>5.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>...</th>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>128</th>\n",
              "      <td>CHEMBL2146517</td>\n",
              "      <td>COC(=O)[C@@]1(C)CCCc2c1ccc1c2C(=O)C(=O)c2c(C)c...</td>\n",
              "      <td>10600.0</td>\n",
              "      <td>inactive</td>\n",
              "      <td>338.359</td>\n",
              "      <td>3.40102</td>\n",
              "      <td>0.0</td>\n",
              "      <td>5.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>129</th>\n",
              "      <td>CHEMBL187460</td>\n",
              "      <td>C[C@H]1COC2=C1C(=O)C(=O)c1c2ccc2c1CCCC2(C)C</td>\n",
              "      <td>10100.0</td>\n",
              "      <td>inactive</td>\n",
              "      <td>296.366</td>\n",
              "      <td>3.44330</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>130</th>\n",
              "      <td>CHEMBL363535</td>\n",
              "      <td>Cc1coc2c1C(=O)C(=O)c1c-2ccc2c(C)cccc12</td>\n",
              "      <td>11500.0</td>\n",
              "      <td>inactive</td>\n",
              "      <td>276.291</td>\n",
              "      <td>4.09564</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>131</th>\n",
              "      <td>CHEMBL227075</td>\n",
              "      <td>Cc1cccc2c3c(ccc12)C1=C(C(=O)C3=O)[C@@H](C)CO1</td>\n",
              "      <td>10700.0</td>\n",
              "      <td>inactive</td>\n",
              "      <td>278.307</td>\n",
              "      <td>3.29102</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>132</th>\n",
              "      <td>CHEMBL45830</td>\n",
              "      <td>CC(C)C1=Cc2ccc3c(c2C(=O)C1=O)CCCC3(C)C</td>\n",
              "      <td>78900.0</td>\n",
              "      <td>inactive</td>\n",
              "      <td>282.383</td>\n",
              "      <td>4.10530</td>\n",
              "      <td>0.0</td>\n",
              "      <td>2.0</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>133 rows × 8 columns</p>\n",
              "</div>"
            ],
            "text/plain": [
              "    molecule_chembl_id  ... NumHAcceptors\n",
              "0         CHEMBL187579  ...           5.0\n",
              "1         CHEMBL188487  ...           2.0\n",
              "2         CHEMBL185698  ...           4.0\n",
              "3         CHEMBL426082  ...           3.0\n",
              "4         CHEMBL187717  ...           5.0\n",
              "..                 ...  ...           ...\n",
              "128      CHEMBL2146517  ...           5.0\n",
              "129       CHEMBL187460  ...           3.0\n",
              "130       CHEMBL363535  ...           3.0\n",
              "131       CHEMBL227075  ...           3.0\n",
              "132        CHEMBL45830  ...           2.0\n",
              "\n",
              "[133 rows x 8 columns]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 10
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "UXMuFQoQ4pZF"
      },
      "source": [
        "# https://github.com/chaninlab/estrogen-receptor-alpha-qsar/blob/master/02_ER_alpha_RO5.ipynb\n",
        "\n",
        "import numpy as np\n",
        "\n",
        "def pIC50(input):\n",
        "    pIC50 = []\n",
        "\n",
        "    for i in input['standard_value_norm']:\n",
        "        molar = i*(10**-9) # Converts nM to M\n",
        "        pIC50.append(-np.log10(molar))\n",
        "\n",
        "    input['pIC50'] = pIC50\n",
        "    x = input.drop('standard_value_norm', 1)\n",
        "        \n",
        "    return x"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "WU5Fh1h2OaJJ"
      },
      "source": [
        "Point to note: Values greater than 100,000,000 will be fixed at 100,000,000 otherwise the negative logarithmic value will become negative."
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "QuUTFUpcR1wU",
        "outputId": "9d1db8ff-8de4-4dd6-8259-6a28617538eb",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 170
        }
      },
      "source": [
        "df_combined.standard_value.describe()"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "count    1.330000e+02\n",
              "mean     8.017926e+12\n",
              "std      3.344888e+13\n",
              "min      5.000000e+01\n",
              "25%      1.070000e+04\n",
              "50%      2.350000e+04\n",
              "75%      3.000000e+05\n",
              "max      3.311311e+14\n",
              "Name: standard_value, dtype: float64"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 133
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "QyiJ0to5N6Z_",
        "outputId": "e10f18e8-1255-4636-bf2f-efbd3befde4f",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        }
      },
      "source": [
        "-np.log10( (10**-9)* 100000000 )"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "1.0"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 134
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "9S1aJkOYOP6K",
        "outputId": "85aa8a89-99f7-4d9e-dac5-3f599c2fb364",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        }
      },
      "source": [
        "-np.log10( (10**-9)* 10000000000 )"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "-1.0"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 135
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "iktHDDwtPDwl"
      },
      "source": [
        "def norm_value(input):\n",
        "    norm = []\n",
        "\n",
        "    for i in input['standard_value']:\n",
        "        if i > 100000000:\n",
        "          i = 100000000\n",
        "        norm.append(i)\n",
        "\n",
        "    input['standard_value_norm'] = norm\n",
        "    x = input.drop('standard_value', 1)\n",
        "        \n",
        "    return x"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "EkrTs7RfPsrH"
      },
      "source": [
        "We will first apply the norm_value() function so that the values in the standard_value column is normalized."
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "EX2Mj2-ZP1Rj",
        "outputId": "7f0f6cb0-d251-4208-fbf8-19970978625e",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 487
        }
      },
      "source": [
        "df_norm = norm_value(df_combined)\n",
        "df_norm"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>molecule_chembl_id</th>\n",
              "      <th>canonical_smiles</th>\n",
              "      <th>bioactivity_class</th>\n",
              "      <th>MW</th>\n",
              "      <th>LogP</th>\n",
              "      <th>NumHDonors</th>\n",
              "      <th>NumHAcceptors</th>\n",
              "      <th>standard_value_norm</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>CHEMBL187579</td>\n",
              "      <td>Cc1noc(C)c1CN1C(=O)C(=O)c2cc(C#N)ccc21</td>\n",
              "      <td>intermediate</td>\n",
              "      <td>281.271</td>\n",
              "      <td>1.89262</td>\n",
              "      <td>0.0</td>\n",
              "      <td>5.0</td>\n",
              "      <td>7200.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>CHEMBL188487</td>\n",
              "      <td>O=C1C(=O)N(Cc2ccc(F)cc2Cl)c2ccc(I)cc21</td>\n",
              "      <td>intermediate</td>\n",
              "      <td>415.589</td>\n",
              "      <td>3.81320</td>\n",
              "      <td>0.0</td>\n",
              "      <td>2.0</td>\n",
              "      <td>9400.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>CHEMBL185698</td>\n",
              "      <td>O=C1C(=O)N(CC2COc3ccccc3O2)c2ccc(I)cc21</td>\n",
              "      <td>inactive</td>\n",
              "      <td>421.190</td>\n",
              "      <td>2.66050</td>\n",
              "      <td>0.0</td>\n",
              "      <td>4.0</td>\n",
              "      <td>13500.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>CHEMBL426082</td>\n",
              "      <td>O=C1C(=O)N(Cc2cc3ccccc3s2)c2ccccc21</td>\n",
              "      <td>inactive</td>\n",
              "      <td>293.347</td>\n",
              "      <td>3.63080</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "      <td>13110.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>CHEMBL187717</td>\n",
              "      <td>O=C1C(=O)N(Cc2cc3ccccc3s2)c2c1cccc2[N+](=O)[O-]</td>\n",
              "      <td>intermediate</td>\n",
              "      <td>338.344</td>\n",
              "      <td>3.53900</td>\n",
              "      <td>0.0</td>\n",
              "      <td>5.0</td>\n",
              "      <td>2000.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>...</th>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>128</th>\n",
              "      <td>CHEMBL2146517</td>\n",
              "      <td>COC(=O)[C@@]1(C)CCCc2c1ccc1c2C(=O)C(=O)c2c(C)c...</td>\n",
              "      <td>inactive</td>\n",
              "      <td>338.359</td>\n",
              "      <td>3.40102</td>\n",
              "      <td>0.0</td>\n",
              "      <td>5.0</td>\n",
              "      <td>10600.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>129</th>\n",
              "      <td>CHEMBL187460</td>\n",
              "      <td>C[C@H]1COC2=C1C(=O)C(=O)c1c2ccc2c1CCCC2(C)C</td>\n",
              "      <td>inactive</td>\n",
              "      <td>296.366</td>\n",
              "      <td>3.44330</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "      <td>10100.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>130</th>\n",
              "      <td>CHEMBL363535</td>\n",
              "      <td>Cc1coc2c1C(=O)C(=O)c1c-2ccc2c(C)cccc12</td>\n",
              "      <td>inactive</td>\n",
              "      <td>276.291</td>\n",
              "      <td>4.09564</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "      <td>11500.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>131</th>\n",
              "      <td>CHEMBL227075</td>\n",
              "      <td>Cc1cccc2c3c(ccc12)C1=C(C(=O)C3=O)[C@@H](C)CO1</td>\n",
              "      <td>inactive</td>\n",
              "      <td>278.307</td>\n",
              "      <td>3.29102</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "      <td>10700.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>132</th>\n",
              "      <td>CHEMBL45830</td>\n",
              "      <td>CC(C)C1=Cc2ccc3c(c2C(=O)C1=O)CCCC3(C)C</td>\n",
              "      <td>inactive</td>\n",
              "      <td>282.383</td>\n",
              "      <td>4.10530</td>\n",
              "      <td>0.0</td>\n",
              "      <td>2.0</td>\n",
              "      <td>78900.0</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>133 rows × 8 columns</p>\n",
              "</div>"
            ],
            "text/plain": [
              "    molecule_chembl_id  ... standard_value_norm\n",
              "0         CHEMBL187579  ...              7200.0\n",
              "1         CHEMBL188487  ...              9400.0\n",
              "2         CHEMBL185698  ...             13500.0\n",
              "3         CHEMBL426082  ...             13110.0\n",
              "4         CHEMBL187717  ...              2000.0\n",
              "..                 ...  ...                 ...\n",
              "128      CHEMBL2146517  ...             10600.0\n",
              "129       CHEMBL187460  ...             10100.0\n",
              "130       CHEMBL363535  ...             11500.0\n",
              "131       CHEMBL227075  ...             10700.0\n",
              "132        CHEMBL45830  ...             78900.0\n",
              "\n",
              "[133 rows x 8 columns]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 13
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "hb1eKrIjRiH9",
        "outputId": "12b12341-df33-4446-e3cc-2a30ee1fe1f8",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 173
        }
      },
      "source": [
        "df_norm.standard_value_norm.describe()"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "count    1.330000e+02\n",
              "mean     2.110164e+07\n",
              "std      4.089714e+07\n",
              "min      5.000000e+01\n",
              "25%      1.070000e+04\n",
              "50%      2.350000e+04\n",
              "75%      3.000000e+05\n",
              "max      1.000000e+08\n",
              "Name: standard_value_norm, dtype: float64"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 14
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "UDKZzmK57YnS",
        "outputId": "9dde74a3-1198-4c52-a913-c0bd57fbbb4e",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 487
        }
      },
      "source": [
        "df_final = pIC50(df_norm)\n",
        "df_final"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>molecule_chembl_id</th>\n",
              "      <th>canonical_smiles</th>\n",
              "      <th>bioactivity_class</th>\n",
              "      <th>MW</th>\n",
              "      <th>LogP</th>\n",
              "      <th>NumHDonors</th>\n",
              "      <th>NumHAcceptors</th>\n",
              "      <th>pIC50</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>CHEMBL187579</td>\n",
              "      <td>Cc1noc(C)c1CN1C(=O)C(=O)c2cc(C#N)ccc21</td>\n",
              "      <td>intermediate</td>\n",
              "      <td>281.271</td>\n",
              "      <td>1.89262</td>\n",
              "      <td>0.0</td>\n",
              "      <td>5.0</td>\n",
              "      <td>5.142668</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>CHEMBL188487</td>\n",
              "      <td>O=C1C(=O)N(Cc2ccc(F)cc2Cl)c2ccc(I)cc21</td>\n",
              "      <td>intermediate</td>\n",
              "      <td>415.589</td>\n",
              "      <td>3.81320</td>\n",
              "      <td>0.0</td>\n",
              "      <td>2.0</td>\n",
              "      <td>5.026872</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>CHEMBL185698</td>\n",
              "      <td>O=C1C(=O)N(CC2COc3ccccc3O2)c2ccc(I)cc21</td>\n",
              "      <td>inactive</td>\n",
              "      <td>421.190</td>\n",
              "      <td>2.66050</td>\n",
              "      <td>0.0</td>\n",
              "      <td>4.0</td>\n",
              "      <td>4.869666</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>CHEMBL426082</td>\n",
              "      <td>O=C1C(=O)N(Cc2cc3ccccc3s2)c2ccccc21</td>\n",
              "      <td>inactive</td>\n",
              "      <td>293.347</td>\n",
              "      <td>3.63080</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "      <td>4.882397</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>CHEMBL187717</td>\n",
              "      <td>O=C1C(=O)N(Cc2cc3ccccc3s2)c2c1cccc2[N+](=O)[O-]</td>\n",
              "      <td>intermediate</td>\n",
              "      <td>338.344</td>\n",
              "      <td>3.53900</td>\n",
              "      <td>0.0</td>\n",
              "      <td>5.0</td>\n",
              "      <td>5.698970</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>...</th>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>128</th>\n",
              "      <td>CHEMBL2146517</td>\n",
              "      <td>COC(=O)[C@@]1(C)CCCc2c1ccc1c2C(=O)C(=O)c2c(C)c...</td>\n",
              "      <td>inactive</td>\n",
              "      <td>338.359</td>\n",
              "      <td>3.40102</td>\n",
              "      <td>0.0</td>\n",
              "      <td>5.0</td>\n",
              "      <td>4.974694</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>129</th>\n",
              "      <td>CHEMBL187460</td>\n",
              "      <td>C[C@H]1COC2=C1C(=O)C(=O)c1c2ccc2c1CCCC2(C)C</td>\n",
              "      <td>inactive</td>\n",
              "      <td>296.366</td>\n",
              "      <td>3.44330</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "      <td>4.995679</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>130</th>\n",
              "      <td>CHEMBL363535</td>\n",
              "      <td>Cc1coc2c1C(=O)C(=O)c1c-2ccc2c(C)cccc12</td>\n",
              "      <td>inactive</td>\n",
              "      <td>276.291</td>\n",
              "      <td>4.09564</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "      <td>4.939302</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>131</th>\n",
              "      <td>CHEMBL227075</td>\n",
              "      <td>Cc1cccc2c3c(ccc12)C1=C(C(=O)C3=O)[C@@H](C)CO1</td>\n",
              "      <td>inactive</td>\n",
              "      <td>278.307</td>\n",
              "      <td>3.29102</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "      <td>4.970616</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>132</th>\n",
              "      <td>CHEMBL45830</td>\n",
              "      <td>CC(C)C1=Cc2ccc3c(c2C(=O)C1=O)CCCC3(C)C</td>\n",
              "      <td>inactive</td>\n",
              "      <td>282.383</td>\n",
              "      <td>4.10530</td>\n",
              "      <td>0.0</td>\n",
              "      <td>2.0</td>\n",
              "      <td>4.102923</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>133 rows × 8 columns</p>\n",
              "</div>"
            ],
            "text/plain": [
              "    molecule_chembl_id  ...     pIC50\n",
              "0         CHEMBL187579  ...  5.142668\n",
              "1         CHEMBL188487  ...  5.026872\n",
              "2         CHEMBL185698  ...  4.869666\n",
              "3         CHEMBL426082  ...  4.882397\n",
              "4         CHEMBL187717  ...  5.698970\n",
              "..                 ...  ...       ...\n",
              "128      CHEMBL2146517  ...  4.974694\n",
              "129       CHEMBL187460  ...  4.995679\n",
              "130       CHEMBL363535  ...  4.939302\n",
              "131       CHEMBL227075  ...  4.970616\n",
              "132        CHEMBL45830  ...  4.102923\n",
              "\n",
              "[133 rows x 8 columns]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 15
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "BoqY53udSTYC",
        "outputId": "65595f1e-9547-4934-e958-b04825cf2316",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 173
        }
      },
      "source": [
        "df_final.pIC50.describe()"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "count    133.000000\n",
              "mean       4.060148\n",
              "std        1.783762\n",
              "min        1.000000\n",
              "25%        3.522879\n",
              "50%        4.628932\n",
              "75%        4.970616\n",
              "max        7.301030\n",
              "Name: pIC50, dtype: float64"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 16
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "HmrndhDW3c7Z",
        "outputId": "e3216e27-a94a-4848-8f18-c1c2533ad00f",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 470
        }
      },
      "source": [
        "df_2class = df_final[df_final.bioactivity_class != 'intermediate']\n",
        "df_2class"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>molecule_chembl_id</th>\n",
              "      <th>canonical_smiles</th>\n",
              "      <th>bioactivity_class</th>\n",
              "      <th>MW</th>\n",
              "      <th>LogP</th>\n",
              "      <th>NumHDonors</th>\n",
              "      <th>NumHAcceptors</th>\n",
              "      <th>pIC50</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>CHEMBL185698</td>\n",
              "      <td>O=C1C(=O)N(CC2COc3ccccc3O2)c2ccc(I)cc21</td>\n",
              "      <td>inactive</td>\n",
              "      <td>421.190</td>\n",
              "      <td>2.66050</td>\n",
              "      <td>0.0</td>\n",
              "      <td>4.0</td>\n",
              "      <td>4.869666</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>CHEMBL426082</td>\n",
              "      <td>O=C1C(=O)N(Cc2cc3ccccc3s2)c2ccccc21</td>\n",
              "      <td>inactive</td>\n",
              "      <td>293.347</td>\n",
              "      <td>3.63080</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "      <td>4.882397</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>5</th>\n",
              "      <td>CHEMBL365134</td>\n",
              "      <td>O=C1C(=O)N(Cc2cc3ccccc3s2)c2c(Br)cccc21</td>\n",
              "      <td>active</td>\n",
              "      <td>372.243</td>\n",
              "      <td>4.39330</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "      <td>6.008774</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>7</th>\n",
              "      <td>CHEMBL190743</td>\n",
              "      <td>O=C1C(=O)N(Cc2cc3ccccc3s2)c2ccc(I)cc21</td>\n",
              "      <td>active</td>\n",
              "      <td>419.243</td>\n",
              "      <td>4.23540</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "      <td>6.022276</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>8</th>\n",
              "      <td>CHEMBL365469</td>\n",
              "      <td>O=C1C(=O)N(Cc2cc3ccccc3s2)c2cccc(Cl)c21</td>\n",
              "      <td>inactive</td>\n",
              "      <td>327.792</td>\n",
              "      <td>4.28420</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "      <td>4.950782</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>...</th>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>128</th>\n",
              "      <td>CHEMBL2146517</td>\n",
              "      <td>COC(=O)[C@@]1(C)CCCc2c1ccc1c2C(=O)C(=O)c2c(C)c...</td>\n",
              "      <td>inactive</td>\n",
              "      <td>338.359</td>\n",
              "      <td>3.40102</td>\n",
              "      <td>0.0</td>\n",
              "      <td>5.0</td>\n",
              "      <td>4.974694</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>129</th>\n",
              "      <td>CHEMBL187460</td>\n",
              "      <td>C[C@H]1COC2=C1C(=O)C(=O)c1c2ccc2c1CCCC2(C)C</td>\n",
              "      <td>inactive</td>\n",
              "      <td>296.366</td>\n",
              "      <td>3.44330</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "      <td>4.995679</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>130</th>\n",
              "      <td>CHEMBL363535</td>\n",
              "      <td>Cc1coc2c1C(=O)C(=O)c1c-2ccc2c(C)cccc12</td>\n",
              "      <td>inactive</td>\n",
              "      <td>276.291</td>\n",
              "      <td>4.09564</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "      <td>4.939302</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>131</th>\n",
              "      <td>CHEMBL227075</td>\n",
              "      <td>Cc1cccc2c3c(ccc12)C1=C(C(=O)C3=O)[C@@H](C)CO1</td>\n",
              "      <td>inactive</td>\n",
              "      <td>278.307</td>\n",
              "      <td>3.29102</td>\n",
              "      <td>0.0</td>\n",
              "      <td>3.0</td>\n",
              "      <td>4.970616</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>132</th>\n",
              "      <td>CHEMBL45830</td>\n",
              "      <td>CC(C)C1=Cc2ccc3c(c2C(=O)C1=O)CCCC3(C)C</td>\n",
              "      <td>inactive</td>\n",
              "      <td>282.383</td>\n",
              "      <td>4.10530</td>\n",
              "      <td>0.0</td>\n",
              "      <td>2.0</td>\n",
              "      <td>4.102923</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>119 rows × 8 columns</p>\n",
              "</div>"
            ],
            "text/plain": [
              "    molecule_chembl_id  ...     pIC50\n",
              "2         CHEMBL185698  ...  4.869666\n",
              "3         CHEMBL426082  ...  4.882397\n",
              "5         CHEMBL365134  ...  6.008774\n",
              "7         CHEMBL190743  ...  6.022276\n",
              "8         CHEMBL365469  ...  4.950782\n",
              "..                 ...  ...       ...\n",
              "128      CHEMBL2146517  ...  4.974694\n",
              "129       CHEMBL187460  ...  4.995679\n",
              "130       CHEMBL363535  ...  4.939302\n",
              "131       CHEMBL227075  ...  4.970616\n",
              "132        CHEMBL45830  ...  4.102923\n",
              "\n",
              "[119 rows x 8 columns]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 17
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "p9vA4-hQQ8sA"
      },
      "source": [
        "---"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "18heJagiyHoF"
      },
      "source": [
        "### **Import library**"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "0Egq_rNsxtIj",
        "outputId": "9a158a1d-ba81-4f2e-9b9e-66ae5ce78916",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 72
        }
      },
      "source": [
        "import seaborn as sns\n",
        "sns.set(style='ticks')\n",
        "import matplotlib.pyplot as plt"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "/usr/local/lib/python3.6/dist-packages/statsmodels/tools/_testing.py:19: FutureWarning: pandas.util.testing is deprecated. Use the functions in the public API at pandas.testing instead.\n",
            "  import pandas.util.testing as tm\n"
          ],
          "name": "stderr"
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "NiarmFbOdG3H"
      },
      "source": [
        "### **Frequency plot of the 2 bioactivity classes**"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "w2Ia0iycdMO2",
        "outputId": "34409d5f-d826-4bcb-8167-2d208fbdf5d8",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 367
        }
      },
      "source": [
        "plt.figure(figsize=(5.5, 5.5))\n",
        "\n",
        "sns.countplot(x='bioactivity_class', data=df_2class, edgecolor='black')\n",
        "\n",
        "plt.xlabel('Bioactivity class', fontsize=14, fontweight='bold')\n",
        "plt.ylabel('Frequency', fontsize=14, fontweight='bold')\n",
        "\n",
        "plt.savefig('plot_bioactivity_class.pdf')"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "image/png": "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\n",
            "text/plain": [
              "<Figure size 396x396 with 1 Axes>"
            ]
          },
          "metadata": {
            "tags": []
          }
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "wB68NKVG0j68"
      },
      "source": [
        "### **Scatter plot of MW versus LogP**\n",
        "\n",
        "It can be seen that the 2 bioactivity classes are spanning similar chemical spaces as evident by the scatter plot of MW vs LogP."
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "F79BNwjF0nub",
        "outputId": "beca351e-2b02-49f9-8712-6ffcdcde425f",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 367
        }
      },
      "source": [
        "plt.figure(figsize=(5.5, 5.5))\n",
        "\n",
        "sns.scatterplot(x='MW', y='LogP', data=df_2class, hue='bioactivity_class', size='pIC50', edgecolor='black', alpha=0.7)\n",
        "\n",
        "plt.xlabel('MW', fontsize=14, fontweight='bold')\n",
        "plt.ylabel('LogP', fontsize=14, fontweight='bold')\n",
        "plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)\n",
        "plt.savefig('plot_MW_vs_LogP.pdf')"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "image/png": "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\n",
            "text/plain": [
              "<Figure size 396x396 with 1 Axes>"
            ]
          },
          "metadata": {
            "tags": []
          }
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "oLAfyRwHyJfX"
      },
      "source": [
        "### **Box plots**"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "1n1uIAivyOkY"
      },
      "source": [
        "#### **pIC50 value**"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "EpPviw0hxue6",
        "outputId": "e152d135-be08-4916-9494-49990106efa9",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 367
        }
      },
      "source": [
        "plt.figure(figsize=(5.5, 5.5))\n",
        "\n",
        "sns.boxplot(x = 'bioactivity_class', y = 'pIC50', data = df_2class)\n",
        "\n",
        "plt.xlabel('Bioactivity class', fontsize=14, fontweight='bold')\n",
        "plt.ylabel('pIC50 value', fontsize=14, fontweight='bold')\n",
        "\n",
        "plt.savefig('plot_ic50.pdf')"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "image/png": "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\n",
            "text/plain": [
              "<Figure size 396x396 with 1 Axes>"
            ]
          },
          "metadata": {
            "tags": []
          }
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "PsOqKyysCZCv"
      },
      "source": [
        "**Statistical analysis | Mann-Whitney U Test**"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "LPdV1vDnWBsh"
      },
      "source": [
        "def mannwhitney(descriptor, verbose=False):\n",
        "  # https://machinelearningmastery.com/nonparametric-statistical-significance-tests-in-python/\n",
        "  from numpy.random import seed\n",
        "  from numpy.random import randn\n",
        "  from scipy.stats import mannwhitneyu\n",
        "\n",
        "# seed the random number generator\n",
        "  seed(1)\n",
        "\n",
        "# actives and inactives\n",
        "  selection = [descriptor, 'bioactivity_class']\n",
        "  df = df_2class[selection]\n",
        "  active = df[df.bioactivity_class == 'active']\n",
        "  active = active[descriptor]\n",
        "\n",
        "  selection = [descriptor, 'bioactivity_class']\n",
        "  df = df_2class[selection]\n",
        "  inactive = df[df.bioactivity_class == 'inactive']\n",
        "  inactive = inactive[descriptor]\n",
        "\n",
        "# compare samples\n",
        "  stat, p = mannwhitneyu(active, inactive)\n",
        "  #print('Statistics=%.3f, p=%.3f' % (stat, p))\n",
        "\n",
        "# interpret\n",
        "  alpha = 0.05\n",
        "  if p > alpha:\n",
        "    interpretation = 'Same distribution (fail to reject H0)'\n",
        "  else:\n",
        "    interpretation = 'Different distribution (reject H0)'\n",
        "  \n",
        "  results = pd.DataFrame({'Descriptor':descriptor,\n",
        "                          'Statistics':stat,\n",
        "                          'p':p,\n",
        "                          'alpha':alpha,\n",
        "                          'Interpretation':interpretation}, index=[0])\n",
        "  filename = 'mannwhitneyu_' + descriptor + '.csv'\n",
        "  results.to_csv(filename)\n",
        "\n",
        "  return results"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "HZmUgOmdYVm5",
        "outputId": "6996e4db-2720-4df7-8691-12a5c06c4020",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 79
        }
      },
      "source": [
        "mannwhitney('pIC50')"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>Descriptor</th>\n",
              "      <th>Statistics</th>\n",
              "      <th>p</th>\n",
              "      <th>alpha</th>\n",
              "      <th>Interpretation</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>pIC50</td>\n",
              "      <td>0.0</td>\n",
              "      <td>1.662636e-10</td>\n",
              "      <td>0.05</td>\n",
              "      <td>Different distribution (reject H0)</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "  Descriptor  Statistics  ...  alpha                      Interpretation\n",
              "0      pIC50         0.0  ...   0.05  Different distribution (reject H0)\n",
              "\n",
              "[1 rows x 5 columns]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 23
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "o2UlCwPmyTBq"
      },
      "source": [
        "#### **MW**"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "ZNlEEsDEx3m6",
        "outputId": "50836563-3a3c-4bb4-9ae6-8db38aeaf6f0",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 367
        }
      },
      "source": [
        "plt.figure(figsize=(5.5, 5.5))\n",
        "\n",
        "sns.boxplot(x = 'bioactivity_class', y = 'MW', data = df_2class)\n",
        "\n",
        "plt.xlabel('Bioactivity class', fontsize=14, fontweight='bold')\n",
        "plt.ylabel('MW', fontsize=14, fontweight='bold')\n",
        "\n",
        "plt.savefig('plot_MW.pdf')"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "image/png": "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O3bw4IMP0rt3byIiIhg6dCivvfZapceTLlmyhNGjR9O3b1+6devGr371Kx5//HEOHz5cqYajR48ydepUbrvtNiIiIrjttttISkoiOzsbp9PpeRTvypUrK02fXDyd8pe//AWn00nfvn0r1ZGcnIzT6fQ8buDi6ZTo6GjPY1SPHTvm6XPjxo10794dp9PJ22+/7ekvKyvLs86WLVuq/NmePHmSpKQkBg4cSEREBLfccguPPPJIleufOXOGRx99lOjoaHr06EFERAR33nknCxYsqPTCj927d3P//ffTr18/IiIiGDBgAJMmTWLPnj2efv74xz8ycOBAbrrpJvr168eYMWN44403qty3mEchLnWirKyM7OxsoOLpiMHBwVWuu23bNhISEti6dSs2m42OHTty5MgR/vznP/P000971vv666/58ccfadu2LWFhYRQVFbFhwwbuu+8+zp07B1QE+H/8x3+Qnp7OqVOn6NSpEzabja1bt+Ln50f37t1p3LgxAK1bt6Z79+5VTqGMHj0am83G6dOn2bp1KwAul4tPPvkEqHj0wKWEh4fTunVroOIvkwv7cDgcjBgxAsDzrBHA01/79u3p37//JfssKCjg3nvv5d133yU3N5fg4GCaNm3K5s2bq/y5lpaWsmnTJs6dO0doaCht2rTh6NGjvPrqq/zpT38CwO12M2nSJL788kt8fX25/vrrKS8v57PPPuPQoUMAvPzyy7z99tucPHmS6667jpYtW7Jv3z4+++yzKvct5tF0itSqCyPPC3x8fHj22WcJDAyscptXXnmF8vJyHA4Hq1evplWrVsyfP5/Fixfz0UcfMXnyZJxOJ1OnTiU0NNQTwl9++SX3338/eXl57Ny5k1tuuYVFixZRVFREo0aNePPNN+nTpw8Ae/fu9fyVcGFOfODAgZXmxC/WoUMHbr31VrZu3cpHH33EHXfcwVdffcWpU6ew2WxVhvjChQs9c+IX9nlBfHw877//PpmZmXz33XfccMMN/Pd//zdQ8UvD19f3kn0uX77c8xfE/PnzGTlypOe4qtKiRQs++ugjrrvuOs+yadOmsWbNGtatW8fTTz/N6dOnKSgoACp+sTgcDqDil2GjRhXxcOEBab/97W8900bFxcWekBfv0khcatWFkWe3bt1o0qQJhmHw/PPPc/To0Sq3ufBne1RUFK1atQLwjFgBMjMzAcjJyWHixIn06tWLG264gfvvv9+zzvHjx4H/f8Jdr169PAEO0K1bt6s6nguP2c3IyKC0tJSPPvoIgFtuucUTeFfixhtvpGfPnkBFaObm5nqOPyYmpsrtLhxXx44dPQEO1R+Xr6+v5yFVEREROJ1O1qxZA8CJEyeAir9GLtQzdOhQRowYQWJiItu2baN9+/YA3HHHHUDFiHzgwIHcd999LF68uNpfzGIejcSlVv3zyPPgwYPcddddnD59mvfff5/f/e53V91vVlYWjz32GOfPn6d58+Z069YNl8vFP/7xD6BiWqAuDB48GLvd7pm62bhxI/D/4X41fvOb3/DNN9+wZs0a2rVrh2EY3HzzzXTp0qW2ygYq5vRff/11oCL827ZtS15eHsePH6/083rzzTdJT09n586dHDx4kI0bN/LJJ59w4MAB/uu//ouxY8cSFhZGRkYGBw4cIDMzk//5n//hww8/ZP369TRr1qxW65Yro5G41Jl/fkBmVc+RBjxv/fn8888972lcu3atpz0iIoJ9+/Z5Ti4uWbKEDz74oNIbhC648IjSnTt38r//+7+e5RfCHqBJkyZAxQm7mvj7+zN8+HCg4l2ip0+fpmXLlgwZMqTa7S7s4+zZs794nvrw4cMJDAyksLCQ1157Dah6fv3i4zp27Bjr1q275HFd7NtvvwUqHueakZHBO++847nU8wLDMPjmm2+IjY0lJSWFFStWcM899wB4Tjzv3r2b6667jqeffpolS5Z4fjGcOHFCUyr1gEbiUqtOnDjBvffeS3l5OQcPHgTAZrN5/iS/lClTpvDAAw+Qm5vL4MGDCQwM9MzD/vrXv8bpdNKoUSPP24oeeughgoOD+emnn37R1yOPPMLGjRspKipi/Pjx/Pu//ztnzpzBZrN5rtcOCwvj4MGDbNiwgdjYWJxOJykpKVXWFxsby7vvvuvZ31133VXpLUqXEhYWBkB+fj7Dhg2jVatWvPXWWzRp0gQ/Pz/GjBnD66+/zpkzZ/Dz86s0fXQp8fHxfPjhhxw7downn3ySP//5z7jdbrKzs/nuu+8uuY3T6WTz5s0cOXKE6OhoysvLPSeAL3C5XNx33300b94ch8OBzWbzXEnUtWtXAN566y0+/vhjOnToQEBAgGdqrFmzZvzbv/1btXVL3dNIXGrV+fPn+fbbb9m7dy++vr707NmTP/3pT/Tt27fKbfr168fSpUu57bbbcLvdHDt2jNDQUBITE5kzZw4AXbp04fnnnyckJITz588TEBDASy+99Iu+OnfuzPvvv8+IESMIDAzk6NGjlJeXc9ttt3nWeeKJJ+jRoweNGzdm79697N+/v9pj6tGjhyeU4fKmUu655x6GDh1Ky5YtOXLkCN9++y0ul8vTHhcX5zmJeccdd3jOBVSldevWvPvuu4wdOxaHw8GxY8coLi5mwIABVW4zefJkYmJisNvtlJSU8Otf/5rf/OY3ldbx9fUlLi6OTp06ceLECQ4fPkxQUBBxcXHMnj0bqHhbT58+fSgrK+PAgQM0atSIW2+9lcWLF2O322v8WUjd0kshRLygrKyMqKgoCgsL+ctf/lJtGItUR9MpIiabOnUqBw8epLCwkK5du3L77bd7uySxMI3ERUzmdDpp3LgxERERPP/885WmakSulEJcRMTCdGJTRMTCFOIiIhamEBcRsTCFuIiIhSnERUQs7P8ArCZrRSrYRh0AAAAASUVORK5CYII=\n",
            "text/plain": [
              "<Figure size 396x396 with 1 Axes>"
            ]
          },
          "metadata": {
            "tags": []
          }
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "wRl2FvgHYqaG",
        "outputId": "182737ed-20ce-414f-850e-9c11af877d71",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 79
        }
      },
      "source": [
        "mannwhitney('MW')"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>Descriptor</th>\n",
              "      <th>Statistics</th>\n",
              "      <th>p</th>\n",
              "      <th>alpha</th>\n",
              "      <th>Interpretation</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>MW</td>\n",
              "      <td>409.5</td>\n",
              "      <td>0.001525</td>\n",
              "      <td>0.05</td>\n",
              "      <td>Different distribution (reject H0)</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "  Descriptor  Statistics         p  alpha                      Interpretation\n",
              "0         MW       409.5  0.001525   0.05  Different distribution (reject H0)"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 25
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "z5hyBhGqyc6J"
      },
      "source": [
        "#### **LogP**"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "liEtkpI4yX9t",
        "outputId": "8aa9b4de-6df6-4da6-ed4c-f9376f290d9f",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 367
        }
      },
      "source": [
        "plt.figure(figsize=(5.5, 5.5))\n",
        "\n",
        "sns.boxplot(x = 'bioactivity_class', y = 'LogP', data = df_2class)\n",
        "\n",
        "plt.xlabel('Bioactivity class', fontsize=14, fontweight='bold')\n",
        "plt.ylabel('LogP', fontsize=14, fontweight='bold')\n",
        "\n",
        "plt.savefig('plot_LogP.pdf')"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "image/png": "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+y174okn9PnnnweposaDE3iNnNPp1NatW3XVVVcFuxQ0AgcPHtS4ceO0ZcuWYJfS6NAzNoDT6VR5ebkkyeVy6YUXXtD48ePlcrn0+uuv+7abO3euxo0bp9GjRys9PV1FRUW+dZs2bVJKSopGjx6tsWPH6ssvv9QzzzwjqfZp0WPGjJHH49H06dP1+uuv69SpU0pMTFRJSYnf/jMyMiRJ27dv1z333KOUlBSlpKTovffes+EngWD4zW9+o5SUFN1+++2aPHmyTpw4IUlauXKlRo8erdGjR2vcuHE6evSoZsyYoZMnT2rMmDG+p4/fc8892rRpk77++mv1799fZ86c8e373//935WdnS1J2rx5s1JTU5WSkqLx48fr73//u/0HazILQdejRw+rrKzMsizLGjJkiDVnzhzLsiyrsLDQ6tOnj2/dsWPHfO9ZsWKF9eijj1qWZVn5+fnWLbfcYu3bt8+yLMs6ffq0dfLkybP2bVmWNW3aNOu1116zLMuyHn/8cSszM9OyLMs6c+aM1b9/f6uwsNA6ceKENWbMGOvw4cOWZVnW4cOHrYEDB1onTpwI1I8AQfTN36v58+dbzz33nPXJJ59YQ4cOtY4cOWJZlmWVlZVZlZWVVmFhodWvXz+/9999991Wbm6uZVmWlZ6ebuXk5FiWZVklJSVWv379rPLycqugoMC68847fb+Xe/bssQYNGmTD0TUcDWKioKZm5MiRkqS4uDg5HA653W51795d77//vt544w1VVFSourrat/3HH3+sW2+9VfHx8ZKkiIgIRUREXLCd5ORkzZw5U/fee6/ef/99devWTXFxcdq8ebMOHjyoBx54wLdtSEiICgoKdN11113Zg0XQrV69WmvWrNGZM2dUUVGh+Ph4eb1ejRkzRu3atZOkeg9zJScnKzs7W0lJSVq7dq1cLpdatmypDz74QAcOHPCbBre6ulpHjx5V27ZtA3JcDQ1hbKDmzZv7vg8LC5PX61VRUZFmz56tlStXqkuXLtq6daumTp16We307dtX5eXl2r17t7Kzs5WSkiJJsixLTqdTy5Ytu6z9w3yff/65li9frqysLMXExGjNmjVasWLFJe/vxz/+sWbPnq3S0lJlZ2fr8ccf960bOHCg5s2bdyXKbpQYM24gysrK1KxZM7Vr1041NTXKysryrevfv7/ef/997d+/X5JUVVWl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\n",
            "text/plain": [
              "<Figure size 396x396 with 1 Axes>"
            ]
          },
          "metadata": {
            "tags": []
          }
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "2KgV5v_oFLXh"
      },
      "source": [
        "**Statistical analysis | Mann-Whitney U Test**"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "B61UsGMIFLuE",
        "outputId": "53899c37-0603-4879-c4ed-25c07b4455d9",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 79
        }
      },
      "source": [
        "mannwhitney('LogP')"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>Descriptor</th>\n",
              "      <th>Statistics</th>\n",
              "      <th>p</th>\n",
              "      <th>alpha</th>\n",
              "      <th>Interpretation</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>LogP</td>\n",
              "      <td>712.5</td>\n",
              "      <td>0.295805</td>\n",
              "      <td>0.05</td>\n",
              "      <td>Same distribution (fail to reject H0)</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "  Descriptor  Statistics  ...  alpha                         Interpretation\n",
              "0       LogP       712.5  ...   0.05  Same distribution (fail to reject H0)\n",
              "\n",
              "[1 rows x 5 columns]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 27
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "4db7LZLRym2k"
      },
      "source": [
        "#### **NumHDonors**"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "iru1JPM1yg5A",
        "outputId": "4ab22853-c3de-4d99-ff3a-05b95f232333",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 367
        }
      },
      "source": [
        "plt.figure(figsize=(5.5, 5.5))\n",
        "\n",
        "sns.boxplot(x = 'bioactivity_class', y = 'NumHDonors', data = df_2class)\n",
        "\n",
        "plt.xlabel('Bioactivity class', fontsize=14, fontweight='bold')\n",
        "plt.ylabel('NumHDonors', fontsize=14, fontweight='bold')\n",
        "\n",
        "plt.savefig('plot_NumHDonors.pdf')"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "image/png": "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\n",
            "text/plain": [
              "<Figure size 396x396 with 1 Axes>"
            ]
          },
          "metadata": {
            "tags": []
          }
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "vM5vZWanFe3c"
      },
      "source": [
        "**Statistical analysis | Mann-Whitney U Test**"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "mS-rOqq7Fd1E",
        "outputId": "6d5609b5-8f4a-4e1b-ac76-841a1d93f212",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 79
        }
      },
      "source": [
        "mannwhitney('NumHDonors')"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>Descriptor</th>\n",
              "      <th>Statistics</th>\n",
              "      <th>p</th>\n",
              "      <th>alpha</th>\n",
              "      <th>Interpretation</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>NumHDonors</td>\n",
              "      <td>299.5</td>\n",
              "      <td>0.000024</td>\n",
              "      <td>0.05</td>\n",
              "      <td>Different distribution (reject H0)</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "   Descriptor  Statistics         p  alpha                      Interpretation\n",
              "0  NumHDonors       299.5  0.000024   0.05  Different distribution (reject H0)"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 30
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "yOYQ3QiSyu7-"
      },
      "source": [
        "#### **NumHAcceptors**"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "yCw6tgNCyxHf",
        "outputId": "e53b4169-d3d6-4b4e-d8cf-d0378ca54ddc",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 367
        }
      },
      "source": [
        "plt.figure(figsize=(5.5, 5.5))\n",
        "\n",
        "sns.boxplot(x = 'bioactivity_class', y = 'NumHAcceptors', data = df_2class)\n",
        "\n",
        "plt.xlabel('Bioactivity class', fontsize=14, fontweight='bold')\n",
        "plt.ylabel('NumHAcceptors', fontsize=14, fontweight='bold')\n",
        "\n",
        "plt.savefig('plot_NumHAcceptors.pdf')"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "image/png": "iVBORw0KGgoAAAANSUhEUgAAAWoAAAFeCAYAAACsM1VYAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4yLjEsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy+j8jraAAAgAElEQVR4nO3de1hUdeI/8Pcw3FQcgfCCXCQ0xwsqGkolrjp421IQzMClRPOymbS6m7tKtZbaYhRZrlia67rW4iVd8UatiZjG9s3LWhpe0BXkPiLXERCB4fz+4MepUYjhcmYO8H49j88jZ86c8x6itx8+56YQBEEAERHJloW5AxAR0S9jURMRyRyLmohI5ljUREQyZ2nuAK1VWVmJlJQU9OzZE0ql0txxiIhaRK/X486dO/Dy8oKtra3Ba+2+qFNSUhAWFmbuGEREbSIuLg4+Pj4Gy9p9Uffs2RNA3Yfr06ePmdMQEbWMVqtFWFiY2Gk/1+6Lun66o0+fPnB1dTVzGiKi1mloCpcHE4mIZI5FTUQkcyxqIiKZY1ETEckci5qISOZY1EREMseiJiKSORZ1J1NUVIRVq1ahuLjY3FGIyEgmLero6GhoNBqo1Wpcv34dAFBcXIxFixZh6tSpmDFjBiIiIlBUVGTKWJ3Knj17cOXKFezZs8fcUYjISCYtan9/f8TFxcHFxUVcplAosHDhQhw7dgxHjhyBm5sbYmJiTBmr0ygqKsKJEycgCAISExM5qiZqJ0xa1D4+PnB2djZYZm9vD19fX/Frb29v5ObmNvh+nU6H7Oxsgz9arVbSzB3Jnj17UFtbCwCora3lqJqonZDVvT5qa2uxe/duaDSaBl/fuXMnYmNjTZyq4/j6669RU1MDAKipqcHJkyexZMkSM6cioqbIqqjXrVuHrl274vnnn2/w9fDwcAQFBRksq7/jFDVtwoQJOH78OGpqamBpaYmJEyeaOxIRGUE2RR0dHY2MjAxs2bIFFhYNz8ioVCqoVCoTJ+s4QkNDceLECQCAhYUFQkNDzZyIiIwhi9PzNmzYgJSUFGzevBnW1tbmjtNhOTo6wt/fHwqFApMmTYKDg4O5IxGREUw6on777bfx1VdfoaCgAPPnz4e9vT0+/PBDbN26FR4eHuIIz9XVFZs3bzZltE4jNDQUmZmZHE0TtSMKQRAEc4dojezsbPj7++PEiRN8cAARtVu/1GWymPogIqLGsaiJiGSORU1EJHMsaiIimWNRExHJHIuaiEjmWNRERDLHoiYikjkWNRGRzLGoiYhkjkVNRCRzLGoiIpljURMRyRyLmohI5ljUREQyx6ImIpI5FjURkcyxqImIZI5FTUQkcyxqIiKZY1ETEckci5qISOZY1EREMseiJiKSORY1EZHMsaiJiGSORU1EJHMsaiIimWNRExHJHIuaiEjmWNRERDLHoiYikjkWNRGRzLGoiYhkjkVNRCRzLGoiIpljURMRyRyLmohI5ljUREQyx6ImIpI5FjURkcyxqImIZI5FTUQkcyxqIiKZY1ETEcmcyYo6OjoaGo0GarUa169fF5enp6cjJCQEU6dORUhICG7dumWqSERE7YLJitrf3x9xcXFwcXExWP7mm2/iN7/5DY4dO4bf/OY3WL16takiERG1C5am2pGPj89DywoLC3HlyhXs2LEDADB9+nSsW7cORUVFcHR0fGh9nU4HnU5nsEyr1UoTWGJJSUk4fvy4yfdbUlICALC3tzf5vgFg8uTJ0Gg0Ztk3UXtlsqJuSF5eHnr37g2lUgkAUCqV6NWrF/Ly8hos6p07dyI2NtbUMTuUoqIiAOYraiJqPrMWdXOFh4cjKCjIYJlWq0VYWJiZErWcRqMxy8gyMjISALB+/XqT75uIWsasRe3s7Izbt29Dr9dDqVRCr9cjPz8fzs7ODa6vUqmgUqlMnJKIyLzMenreI488gsGDB+Po0aMAgKNHj2Lw4MENTnsQEXVWJhtRv/322/jqq69QUFCA+fPnw97eHgkJCXjrrbewatUqfPTRR1CpVIiOjjZVJCKidsFkRf3GG2/gjTfeeGh5//79sW/fPlPFICJqd3hlIhGRzLGoiYhkjkVNRCRzLGoiIpljURMRyRyLmohI5ljUREQyx6ImIpI5FjURkcyxqImIZI5FTUQkcyxqIiKZY1ETEckci5qISOZY1EREMseiJiKSORY1EZHMGf2El7KyMpSXl8Pe3h42NjZITEzEd999h0GDBuHZZ5+VMiMRUadmdFGvXr0aX375Jfbu3YuSkhJERERAoVAAAEpLS7FgwQLJQhIRdWZGT31cvnwZdnZ2GD58OI4dOwYAePTRRyEIAg4ePChZQCKizs7oos7Pz0ffvn0BAKmpqRgwYAC++OILuLq6IicnR7KARESdndFFbWFhgcrKSgBARkYGBg4cCACws7ODIAjSpCMiIuOLul+/fsjMzMS0adNQVlaGoUOHAqgbaffu3VuygEREnZ3RRR0eHg4AuHXrFlQqFQIDA5GamoqioiIMGzZMsoBERJ2d0Wd9BAYGYtCgQcjIyMCoUaPg5OSE2tpa7NixA66urlJmJCLq1Iwq6urqaoSEhKBbt2749NNPxdPyevXqhV69ekkakIioszNq6sPKygq5ubkoLS0VS5qIiEzD6DnqoKAg3Lp1Czdu3JAyDxERPcDoOerCwkIIgoBZs2bB19cXTk5O4msKhQJRUVGSBCQi6uyMLurDhw9DoVBAEAQkJyeLywVBYFETEUnI6KKuvyqRiIhMy+iiTkpKkjIHERE1wuiirnfjxg2kpKQAALy8vPDYY4+1eSgiIvqJ0UVdU1ODlStX4osvvjBY/swzzyA6OhpKpbLNwxERUTNOz/vb3/6GhIQECIJg8CchIQF/+9vfpMxIRNSpGV3UBw8ehEKhwKJFi3Do0CEcOnQICxcu5P2oiYgkZvTUR05ODjw8PPDqq6+Ky9RqNRITE5GdnS1JOCIiasaI2sbGBkVFRSgrKxOX3b17F0VFRbC1tZUkHBERNWNEPWLECHz77bcICAiAn58fACA5ORl3797F2LFjJQtIRNTZGV3US5YswZkzZ5Cbm4t9+/YBqLsq0dLSEi+//LJkAYmIOjujpz58fHywfft2+Pj4wMbGBjY2Nhg9ejT+/ve/Y9SoUVJmJCLq1Jp1wYuvry98fX2lykJERA0wekQ9ePBghIaGPrQ8MjISs2fPbtNQRET0E6NH1I09aTw1NRVXr15ts0BERGSoyaKOjIwU/56ZmWnw9b1793Dt2jXY2NhIk46IiJou6vj4ePHxW8XFxQ9dhSgIAgYNGiRNOiIiarqo6+9DnZeXBysrK4Mnu3Tp0gWenp5Yvnx5q4OcPHkSGzduFO8hEhERgSlTprR6u0RE7V2TRV1/H+pBgwZhyJAh2LNnT5uHEAQBf/rTnxAXF4eBAwfi2rVrmDNnDiZNmgQLC6OPdxIRdUhGH0w8ceIErK2tAQAVFRUAgK5du7ZZEAsLC9y9exdA3aXpvXr1eqikdToddDqdwTKtVttmGYiI5MjoonZxccHu3buxbds25OXlAQCcnZ2xaNEizJkzp1UhFAoFPvzwQ7z88svo2rUrysvL8cknnzy03s6dOxEbG9uqfRERtTdGF3VsbCw2b95scJpebm4u1q5di8LCQkRERLQ4RE1NDbZu3YqPPvoIjz/+OP773/9i+fLlSEhIQLdu3cT1wsPDERQUZPBerVaLsLCwFu+biEjujC7qXbt2QRAEDB8+HJMmTQJQNx1y8eJF7Nq1q1VFffXqVeTn5+Pxxx8HADz++OPo0qULbt68ieHDh4vrqVQqqFSqFu+HiKg9Mrqo7927h169eiEuLg5WVlYAgHnz5mHSpEkoLy9vVYg+ffpAq9UiLS0Nnp6euHnzJgoLC+Hu7t6q7RIRdQRGF/XEiRNx4cIFWFr+9BalUgkLCwtxhN1SPXv2xFtvvYVly5aJ52xHRUXB3t6+VdslIuoIjC7qYcOGITExEfPmzRPPbz5+/Dh0Oh28vLwMLoSZOXNms4MEBAQgICCg2e8jIurojC7q6OhoKBQKnD17FmfPnjV4LSoqSvy7QqFoUVETEVHDmnWb08ZuzERERNJp1gUvRERkes264KVeaWkpampq8Mgjj0gSioiIftKsG2l89dVXmDZtGp544gksXboUJ06cwNy5c3Hq1Cmp8hERdXpGj6hPnjyJ5cuXo7a2Vlw2ZMgQnDt3Dj179sT48eMlCUhE1NkZPaL++OOPIQiCwWO3nJ2d4eTkhEuXLkkSjoiImlHU165dg7u7O9atW2ew3MnJCfn5+W0ejIiI6hhd1FZWVqiurjZYptfrxQcKEBGRNIwu6qFDhyIvLw9//OMfAQCFhYV45ZVXUFJSgmHDhkkWkIioszO6qBcvXgwAOHr0KBQKBbKzs5GUlASFQoEFCxZIFpCIqLMzuqj9/PzwwQcfoG/fvuJzDV1cXPD+++/Dz89PyoxERJ1asy4hnzZtGqZNm4aioiIAgKOjoyShiIjoJ0YX9Q8//IBbt25h9OjR4lWKOTk5OHfuHPr164eRI0dKFpKIqDMzuqjXrl2LtLQ0fPPNN+KyHj164K233sKAAQOwf/9+SQISEXV2Rs9Rp6enw93dHd27dxeX2dnZwd3dHWlpaZKEIyKiZhS1IAi4ffs2qqqqxGVVVVW4ffu2wWXlRETUtowuak9PT+h0OvzhD3/A+fPncf78ebz66qsoLS2Fp6enlBmJiDo1o+eoZ8+ejTVr1uDEiRMG96ZWKBR47rnnJAlHRETNGFHPmTMHYWFhACCeRw0AYWFhCA0NlSYdERE17zzqP//5z3jxxRfx448/Aqh74O3PHyjQ3mzbtq3THQit/7yRkZFmTmJ6np6eWLRokbljEDWb0UWt0+lQVlYGBwcHTJs2DQBw79495Obmws7ODiqVSrKQUklLS0PKlVQobe3NHcVkamuUAICrabfNnMS09JUl5o5A1GJGF/WyZctw9uxZfPnll3B3dwcAFBQUYNq0afD19cXf//53yUJKSWlrj679/M0dgyRWkcFnflL7ZfQc9ZUrV+Du7i6WNAC4ubnB3d0dly9fliQcERE1o6grKipw//79h5bfv38fFRUVbRqKiIh+YnRROzs7Iy8vD9u2bYNer0dtbS22b9+O3NxcODs7S5mRiKhTM7qoJ02aBEEQsGHDBnh7e2PEiBGIiYmBQqHAlClTpMxIRNSpGV3US5cuxZAhQyAIAqqrq1FdXQ1BEDB48GC8/PLLUmYkIurUjD7ro1u3bti7dy8SEhLEp44PHz4czzzzDJ+ZSEQkoWZd8GJlZYWZM2di5syZ4rKioiIcPnwY8+bNa+tsRESEZhZ1Pb1ej6+//hoHDhzAqVOnUFtby6ImIpJIs4r6+vXrOHDgAI4cOSI+jksQBCgUCknCERGREUWt0+lw5MgRHDhwAFeuXAEA8YZMCoUCy5cvx+TJk6VNSUTUiTVZ1GPHjkVNTY1Yzn379sWMGTPw6aeforKyEi+99JLkIYmIOrMmi7q6uhoKhQLDhg3DypUr4ePjAwDYtWuX5OGIiKgZ51GnpKRgzZo12L59O/Lz86XMREREP9NkUf/hD3+Ah4cHBEHAjRs3EBMTg4kTJ6KsrAwAUFxcLHlIIqLOrMmiXrx4Mb788kvs3r0bzz77LLp16wa9Xi/OWfv5+WHu3LmSByUi6qyMnvoYOXIk3n77bSQnJ+Pdd9/FE088AaDunOpz585JFpCIqLNr9gUvtra2CAgIQEBAAHJychAfH4+DBw9KkY2IiNCMEXVDXFxcEBERgcTExLbKQ0RED2hyRG3MQ1AVCgWioqLaJBARERlqsqjj4+ONukScRU1EJA2j5qjrz/AgIiLTa3KO+tq1awZ/AMDb27vB5UREAJCWloaQkBCkp6ebO0qH0KqDiW3p/v37ePPNNzFlyhTMmDEDf/7zn80diYhaKCYmBhUVFYiJiTF3lA6hRfejlsJ7770HGxsbHDt2DAqFAgUFBeaOREQtkJaWhqysLABAZmYm0tPT8eijj5o5VfvWZFHn5uY+tKyqqgp5eXkGc9d9+/ZtcYjy8nIcPHgQp06dEg9cOjk5PbSeTqeDTqczWKbValu83+LiYugrS1CRcaLF26D2QV9ZguJia3PH6BQeHEXHxMRg8+bNZkrTMTRZ1BqNxuCsD4VCgatXr0Kj0Rgsq79XdUtkZWXB3t4esbGxOHPmDLp164Zly5aJd+qrt3PnTsTGxrZ4P0QkvfrRdL3MzEwzJek4ZHHWh16vR1ZWFoYMGYKVK1fi4sWLeOmll3D8+HHY2dmJ64WHhyMoKMjgvVqtFmFhYS3ar4ODA7TFVejaz79V+Un+KjJOwMHBwdwxOgU3NzeDsnZ3dzdjmo6hyaKOiIiQPISzszMsLS0xffp0AMCIESPg4OCA9PR0DBs2TFxPpVJBpVJJnoeIWm7FihVYtmyZwdfUOrIoakdHR/j6+uI///kP/Pz8kJ6ejsLCQvTr10/yfRNR2/L09BRH1e7u7jyQ2AaafdZHVVUVCgsLH5oOac3BRABYs2YNXnvtNURHR8PS0hLvvvsuR89E7dSKFSsQGRnJ0XQbMbqo09PT8frrr+P7779/6LXWHkwE6ua1Pvvss1Ztg4jkwdPTE3v37jV3jA7D6KJ+/fXXceHCBSmzEBFRA4wu6qtXr8LKygoLFy6Em5ubUTdqIiKi1jO6qPv374/y8nKDo7lERCQ9o4t67dq1WLBgAVavXo2JEycanN8MAKNHj27zcERE1IyivnfvHiwsLLBv3z7s27fP4LW2OJhIREQNM7qo33rrLRQVFfHe1EREJmZ0UWdlZaFLly6IjIyEq6srlEqllLmIiOj/M7qo/fz8kJqaitmzZ0uZh4iIHmB0UY8aNQqnT5/GokWLMH78+IcOJs6cObPNwxERUTOK+t1334VCoUBycjKSk5MNXlMoFCxqIiKJNOteHzyQSERkekYX9YkTfAoKEZE5GF3ULi4uUuYgIqJGGF3UkZGRjb6mUCgQFRXVJoGIiMiQ0UUdHx/f4I2YBEFgURMRScjoon7wwQBlZWXQ6XSwsLCAs7NzmwcjIqI6Rhd1UlLSQ8vOnDmDJUuW4JVXXmnTUERE9BOL1rzZ19cXXl5e2Lp1a1vlISKiBxg9oj548KDB13q9HpmZmbhw4QKsrKzaPBgREdUxuqhXrVrV6MHEkSNHtmkoIiL6SauvTPT29sa6devaLBARtY2kpCQcP37cLPsuKSkBANjb25tl/5MnT4ZGozHLvqXQ4isTFQoFHnnkEdjY2LR5KCJq34qKigCYr6g7miaLOi4uzqgNhYWFtToMEbUdjUZjtlFl/QVy69evN8v+O5omi3rdunVGPXGcRU1EJA2jpj6aumueMUVOREQt02RRN3TXvP/973/YuHGj+EDbgQMHtn0yIiICYERR//yueVqtFn/9619x+PBh1NTUwNXVFb/73e8wY8YMSUMSEXVmRk19lJSUYMuWLdi9ezfu378PJycnLFmyBCEhIbC0bNYZfkRE1ExNtuzmzZuxY8cOlJeXo3v37liyZAnmzZsHW1tbU+QjIur0mizqTZs2iQcL7e3tkZiYiMTERIN1FAoF9u3bJ01CIqJOzuh5C0EQkJWVJf7953jWBxGRdJos6tGjR5siBxERNaLJov7ss89MkYOIiBrRqvtRExGR9FjUREQyx6ImIpI5FjURkcyxqImIZI5FTUQkcyxqIiKZY1ETEckci5qISOZY1EREMseiJiKSORY1EZHMya6oY2NjoVarcf36dXNHISKSBVkV9eXLl/HDDz8YPKeRiKizk80DD6uqqrB27Vq8//77mDt3boPr6HQ66HQ6g2VarbZV+9VXlqAi4+EnrXdUtTWVAAALy871KDV9ZQmA3ibf7+rVq5Gammry/ZpbZWXdz1lISIiZk5iWWq3G2rVr23y7sinqjRs3IiAgAK6uro2us3PnTsTGxrbZPj09PdtsW+1FWloaAMDT0/SlZV69zfLfOz8/H/cqKmCt7FxPQbJA3VOg9PfvmTmJ6VTpBeTn50uybVkU9ffff4+UlBSsWLHiF9cLDw9HUFCQwTKtVouwsLAW7XfRokUtel97FhkZCQBYv369mZN0Dg4ODrAsy8f84Y7mjkIS23GpCN0dHCTZtiyK+ty5c7h58yb8/f0B1JXvggULsH79evj5+YnrqVQqqFQqc8UkIjILWRT14sWLsXjxYvFrjUaDLVu2YODAgWZMRUQkD7I664OIiB4mixH1g5KSkswdgYhINjiiJiKSORY1EZHMsaiJiGSORU1EJHMsaiIimWNRExHJHIuaiEjmWNRERDLHoiYikjkWNRGRzLGoiYhkjkVNRCRzLGoiIpljURMRyRyLmohI5ljUREQyx6ImIpI5FjURkcyxqImIZI5FTUQkcyxqIiKZk+VTyIk6Em1ZDXZcKjL5fsuqalFWVWvy/cqBnbUF7KxNOw7VltWgu0TbZlETScjT09Ns+64pLsa94mKz7d+cbB0c0N3BwaT77A7p/nuzqIkktGjRInNHoA6Ac9RERDLHoiYikjkWNRGRzLGoiYhkjkVNRCRzLGoiIpljURMRyRyLmohI5ljUREQyx6ImIpI5FjURkcyxqImIZI5FTUQkcyxqIiKZY1ETEckci5qISOZY1EREMseiJiKSORY1EZHMsaiJiGSORU1EJHMsaiIimbM0dwAAKC4uxp/+9CdkZmbC2toa/fr1w9q1a+Ho6GjuaEREZieLEbVCocDChQtx7NgxHDlyBG5uboiJiTF3LCIiWZDFiNre3h6+vr7i197e3ti9e/dD6+l0Ouh0OoNlWq1W8nxSSEpKwvHjx02+37S0NABAZGSkyfcNAJMnT4ZGozHLvonaK1kU9c/V1tZi9+7dDf7PvHPnTsTGxpohVcfB6SSi9kd2Rb1u3Tp07doVzz///EOvhYeHIygoyGCZVqtFWFiYqeK1GY1Gw5ElERlFVkUdHR2NjIwMbNmyBRYWD0+fq1QqqFQqMyQjIjIf2RT1hg0bkJKSgk8++QTW1tbmjkNEJBuyKOobN25g69at8PDwQGhoKADA1dUVmzdvNnMyIiLzk0VRP/bYY0hNTTV3DCIiWZLFedRERNQ4FjURkcyxqImIZI5FTUQkcyxqIiKZY1ETEcmcLE7Paw29Xg+g/d6ciYgI+KnD6jvt59p9Ud+5cwcA2uX9PoiIHnTnzh3069fPYJlCEATBTHnaRGVlJVJSUtCzZ08olUpzx5G9+ptYxcXFoU+fPuaOQx0Uf86aT6/X486dO/Dy8oKtra3Ba+1+RG1rawsfHx9zx2h3+vTpA1dXV3PHoA6OP2fN8+BIuh4PJhIRyRyLmohI5ljUREQyx6LuZFQqFSIiIvgABpIUf87aVrs/64OIqKPjiJqISOZY1EREMseiJiKSORa1zAUGBqKyslKSbW/atAlVVVXi1xs3bsQXX3whyb6o49PpdNi2bZvBstdffx3nz583U6KOgwcTOzG1Wo0LFy6gW7du5o5CHUB2djZmzZqFM2fOmDtKh8MRtcyp1WqUl5cDADQaDTZu3IiQkBBoNBr885//FNeLjo7GrFmzEBAQgPDwcOTk5IivnTx5EsHBwQgICMDMmTNx7do1rFmzBgAQGhqKwMBA6HQ6rFq1Cv/85z9x7949+Pr6oqioyGD7sbGxAICLFy/ihRdeQHBwMIKDg/H111+b4DtB5vDqq68iODgYM2bMwNKlS1FaWgoA2L9/PwICAhAQEIBZs2ahoKAAa9euxd27dxEYGIjQ0FAAwAsvvICTJ08iNzcXY8eORXV1tbjt3/3ud4iPjwcAnDp1CqGhoQgODkZISAh++OEH039YORNI1gYOHCiUlZUJgiAIEydOFN555x1BEAQhKytL8Pb2Fl8rLCwU3/P5558Ly5cvFwRBENLS0oSnnnpKSE9PFwRBEO7fvy/cvXv3oW0LgiCsXLlS+OyzzwRBEITXXntN2LlzpyAIglBdXS2MHTtWyMrKEkpLS4XAwEDh9u3bgiAIwu3bt4Vx48YJpaWlUn0LyIx+/nO1YcMG4b333hO+++47YdKkSUJ+fr4gCIJQVlYmVFZWCllZWcKYMWMM3v/8888LSUlJgiAIQnh4uJCYmCgIgiAUFRUJY8aMEcrLy4WMjAzhueeeE38ur1+/LowfP94En679aPc3Zepsnn76aQCAq6srVCoVtFot+vfvj9OnT2PXrl2oqKhATU2NuP63336LX/3qV/Dw8AAAWFtbw9rausn9BAUF4S9/+Qvmzp2L06dPw9PTE66urjh16hSys7OxaNEicV2FQoGMjAwMGzasbT8smd2hQ4dw5MgRVFdXo6KiAh4eHtDr9QgMDETPnj0BwOips6CgIMTHx8Pf3x9Hjx6FRqNB165d8c033yAzM9PgVsU1NTUoKCiAk5OTJJ+rvWFRtzM2Njbi35VKJfR6PXJycrB+/Xrs378fbm5uuHDhAlasWNGq/fj4+KC8vBypqamIj49HcHAwAEAQBKjVasTFxbVq+yR/58+fx+7du7Fnzx44OjriyJEj+Pzzz1u8vSlTpmD9+vUoLi5GfHw8XnvtNfG1cePG4d13322L2B0S56g7gLKyMlhZWaFnz56ora3Fnj17xNfGjh2L06dP49atWwCAqqoqlJWVAagbCdX/vSEzZ87Ejh07cO7cOUydOhUAMHLkSGRkZOC7774T17t06RIEHpPucHQ6Hezs7GBvb4+qqir861//AgBMmDABhw4dQkFBAQCgvLwc9+/fh52dHSorKw1+o/u5Ll26wN/fHxs2bEBZWZl4e+KxY8fim2++wY0bN8R1L126JPGna184ou4A1Go1pk2bhqeffhoODg4YP368eEqUh4cH1q1bh9///vfQ6/VQKpV45513oFar8eKLL2Lu3LmwtbXFZ5999tB2Z86cCX9/fwQHB6NLly4AgB49euCjjz7Ce++9h6ioKFRXV8PNzQ1btmyBQqEw6ecmaY0bNw6HDx/G1KlT4eDgAB8fH/z444/w9fXF4sWLMX/+fCgUClhbW2PLli1wcnLCjBkzMGPGDPTo0cNgwFAvKCgIYRGnY38AAAm0SURBVGFhWLZsmbjMw8MD7733Hl5//XVUVlaiuroao0aNwvDhw035cWWNp+cREckcpz6IiGSORU1EJHMsaiIimWNRExHJHIuaiEjmWNTU5s6cOQO1Wg21Wi27G/Rs2rRJzNYcq1atglqthkajkSiZceqzb9q0yaw5yLR4HjUZ7YUXXsDZs2fFr5VKJezt7TF8+HAsX74cgwYNAgDY2dlhxIgR4t/NQaPRICcnB0FBQXjnnXfE5X369BGzNYebmxtGjBghXjYN1JV3fHw8XFxckJSU1Ca5iRrCoqZms7KywpAhQ1BVVYXU1FScPHkSly5dQlJSEmxtbTF06NBWXWospdmzZ2P27NnNft/SpUuxdOlSCRIRNY1TH9RsvXr1wueff46DBw8iIiICAFBYWIj//e9/ABqf+jh//jwWLFiAxx9/HF5eXpg6dSo+/vhjg1tfbt++HYGBgRgzZgyGDh2KJ554AhEREUhPTzfIkJGRgRUrVsDPzw9eXl7w8/PD6tWrkZ2dDbVaLd7mNT4+3mCq48Gpj08++QRqtRpjxowxyLF27Vqo1Wrx0vkHpz40Go14i86cnBxxm4mJiRgxYgTUajV27dolbi8rK0tc5/Tp041+bwsKCrB69WpMmDABXl5eePLJJ/HSSy81un5FRQVefvllaDQaeHt7w8vLC1OmTMHGjRsNHgpx6dIlzJ8/H76+vvDy8sL48eOxePFi/Pjjj+J21qxZgwkTJmDYsGHw9fXF7NmzsWPHjkb3TabDoqYWq6qqQnZ2NoC6u/L17du30XXPnDmD8PBwJCcnw8LCAi4uLrh16xY+/PBDrFy5Ulzv7NmzyMzMhJOTEzw9PaHT6XD8+HHMmzcP9+/fB1BX0s8++yyOHDmCwsJCuLm5wcLCAsnJybC2tsaIESNgZWUFAHBwcMCIESMane4IDAyEhYUFSktLkZycDADQ6/X497//DaDuMvqGDB48GA4ODgDqfsOo34ezszOmT58OAOK9MQCI2+vVqxfGjh3b4DaLi4vx3HPPYe/evcjLy0Pfvn3RpUsXnDx5stHva2VlJU6cOIH79+/Dw8MDjzzyCDIyMvDRRx/hgw8+AADU1tZi8eLF+Pbbb6FUKvHYY4+hpqYGp06dQlpaGgDgr3/9K3bt2oWCggIMGDAA3bt3x5UrV3Dq1KlG902mw6kParb6EWQ9hUKBdevWwdHRsdH3bNq0CTU1NXB2dsahQ4fQo0cPxMTEYNu2bUhISMBvf/tbqNVqrFixAh4eHmLRfvvtt5g/fz60Wi0uXLiAJ598Elu2bIFOp4OlpSX+8Y9/YPTo0QCAy5cvi6P9+jnqCRMmGMxRP6h379546qmnkJycjISEBEycOBHfffcdCgsLYWFh0WhRb968WZyjrt9nvbCwMOzfvx8pKSm4du0aBg0ahK+++gpA3T8MSqWywW3GxcWJvwnExMRgxowZ4udqjJ2dHRISEjBgwABx2R//+EccPnwYX3zxBVauXInS0lIUFxcDqPvHw9nZGUDdP3iWlnUVUH/TriVLlohTPGVlZWKRk3lxRE3NVj+CHDp0KGxtbSEIAqKiopCRkdHoe+p/xR43bhx69OgBAOLIEwBSUlIAALm5uZg7dy5GjRqFQYMGYf78+eI6t2/fBvDTndVGjRolljQADB06tEWfp/4WrklJSaisrERCQgIA4MknnxRLrTmGDBmCkSNHAqgrxry8PPHzBwUFNfq++s/l4uIiljTwy59LqVSKN07y8vKCWq3G4cOHAQD5+fkA6n6rqM8zdepUTJ8+HcuWLcOZM2fQq1cvAMDEiRMB1I2sJ0yYgHnz5mHbtm2/+I8vmQ5H1NRsPx9B3rx5E08//TRKS0uxf/9+vPrqqy3eblZWFpYuXYrq6mp069YNQ4cOhV6vx9WrVwHU/QovhUmTJkGlUonTLImJiQB+KvCWmDNnDr7//nscPnwYPXv2hCAIGD58OPr3799WsQHUzbFv3boVQF3BOzk5QavV4vbt2wbfr3/84x84cuQILly4gJs3byIxMRH//ve/cf36dbzxxhsICQmBp6cnkpKScP36daSkpOD//u//cODAARw7dgxdu3Zt09zUPBxRU6v8/OaLjd2HGID49JdvvvlGfO7e0aNHxde9vLxw5coV8YDe9u3b8a9//cvgSTL16m9/eeHCBfz3v/8Vl9cXOgDY2toCqDtI1hQbGxv8+te/BlD3bMjS0lJ0794dkydP/sX31e/j3r17D92P+9e//jUcHR1RUlKCjz/+GEDj890Pfq6cnByDp8H//HM96OLFiwDqbhWalJSE3bt3i6dJ1hMEAd9//z2Cg4Oxfv16fP7555g1axYAiAd7L126hAEDBmDlypXYvn27WP75+fmc/pABjqip2fLz8/Hcc8+hpqYGN2/eBABYWFiIvz435JVXXsGLL76IvLw8TJo0CY6OjuK86DPPPAO1Wg1LS0vxqTULFy5E3759cefOnYe29dJLLyExMRE6nQ7PP/88Hn30UVRUVMDCwkI8n9nT0xM3b97E8ePHERwcDLVajfXr1zeaLzg4GHv37hX39/TTTxs8Tachnp6eAICioiJMmzYNPXr0wKeffgpbW1tYW1tj9uzZ2Lp1KyoqKmBtbW0w1dOQsLAwHDhwADk5Ofj973+PDz/8ELW1tcjOzsa1a9cafI9arcbJkydx69YtaDQa1NTUiAdd6+n1esybNw/dunWDs7MzLCwsxDN0Bg4cCAD49NNP8eWXX6J3796wt7cXp7G6du0Kd3f3X8xN0uOImpqturoaFy9exOXLl6FUKjFy5Eh88MEHGDNmTKPv8fX1xc6dO+Hn54fa2lrk5OTAw8MDy5YtQ3R0NACgf//+iIqKgqurK6qrq2Fvb48NGzY8tK1+/fph//79mD59OhwdHZGRkYGamhr4+fmJ6yxfvhze3t6wsrLC5cuXkZqa+oufydvbWyxewLhpj1mzZmHq1Kno3r07bt26hYsXL0Kv14uvh4aGigcOJ06cKM7NN8bBwQF79+5FSEgInJ2dkZOTg7KyMowfP77R9/z2t79FUFAQVCoVysvL8cwzz2DOnDkG6yiVSoSGhsLNzQ35+flIT09Hnz59EBoaijfffBNA3VNbRo8ejaqqKly/fh2WlpZ46qmnsG3bNqhUqia/FyQtPjiASCJVVVUYN24cSkpK8Mknn/xi4RL9Ek59EElgxYoVuHnzJkpKSjBw4ED86le/Mnckasc4oiaSgFqthpWVFby8vBAVFWUwrULUXCxqIiKZ48FEIiKZY1ETEckci5qISOZY1EREMseiJiKSuf8HijDxI2P4KEAAAAAASUVORK5CYII=\n",
            "text/plain": [
              "<Figure size 396x396 with 1 Axes>"
            ]
          },
          "metadata": {
            "tags": []
          }
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "NEQoDZctFtGG",
        "outputId": "eb994475-ed64-4633-c67b-a88e2c3ecc48",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 79
        }
      },
      "source": [
        "mannwhitney('NumHAcceptors')"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>Descriptor</th>\n",
              "      <th>Statistics</th>\n",
              "      <th>p</th>\n",
              "      <th>alpha</th>\n",
              "      <th>Interpretation</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>NumHAcceptors</td>\n",
              "      <td>415.0</td>\n",
              "      <td>0.001557</td>\n",
              "      <td>0.05</td>\n",
              "      <td>Different distribution (reject H0)</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "      Descriptor  Statistics  ...  alpha                      Interpretation\n",
              "0  NumHAcceptors       415.0  ...   0.05  Different distribution (reject H0)\n",
              "\n",
              "[1 rows x 5 columns]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 32
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "p4QjdHVjKYum"
      },
      "source": [
        "#### **Interpretation of Statistical Results**"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "U-rK8l0wWnKK"
      },
      "source": [
        "## **Zip files**"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "GW1ZSsfJWqbM",
        "outputId": "def6e823-0194-4848-fb5e-0d86e1ad88f4",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 243
        }
      },
      "source": [
        "! zip -r results.zip . -i *.csv *.pdf"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "  adding: mannwhitneyu_NumHAcceptors.csv (deflated 12%)\n",
            "  adding: mannwhitneyu_NumHDonors.csv (deflated 9%)\n",
            "  adding: plot_LogP.pdf (deflated 37%)\n",
            "  adding: mannwhitneyu_LogP.csv (deflated 7%)\n",
            "  adding: plot_MW_vs_LogP.pdf (deflated 15%)\n",
            "  adding: plot_ic50.pdf (deflated 37%)\n",
            "  adding: plot_NumHDonors.pdf (deflated 38%)\n",
            "  adding: plot_NumHAcceptors.pdf (deflated 37%)\n",
            "  adding: plot_MW.pdf (deflated 38%)\n",
            "  adding: mannwhitneyu_pIC50.csv (deflated 10%)\n",
            "  adding: bioactivity_data_preprocessed.csv (deflated 80%)\n",
            "  adding: plot_bioactivity_class.pdf (deflated 38%)\n",
            "  adding: mannwhitneyu_MW.csv (deflated 9%)\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "LMWOG2UIXEg-"
      },
      "source": [
        ""
      ],
      "execution_count": null,
      "outputs": []
    }
  ]
}