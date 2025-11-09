from pathlib import Path
import shutil

def get_data():
    """
    Vérifie que le fichier CSV brut existe dans data/raw/.
    Si non, copie depuis un emplacement local.
    """
    raw_path = Path("data/raw/etat-du-trafic-en-temps-reel.csv")
    raw_path.parent.mkdir(parents=True, exist_ok=True)

    if raw_path.exists():
        print(f"✅ Fichier déjà présent : {raw_path}")
    else:
        # Exemple : copie depuis un dossier local 'source_data'
        source = Path("source_data/etat-du-trafic-en-temps-reel.csv")
        if source.exists():
            shutil.copy(source, raw_path)
            print(f"✅ Fichier copié depuis {source}")
        else:
            raise FileNotFoundError(f"❌ Aucun fichier trouvé à {raw_path} ni {source}")

if __name__ == "__main__":
    get_data()
