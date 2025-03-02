import asyncio
import json
import logging
from collections import Counter
from pathlib import Path
from typing import List, Dict, Any, Optional

import matplotlib.pyplot as plt

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EmotionAnalyzer:
    """
    Класс для анализа эмоций в текстах выступлений.

    :val emotion_synonyms: Словарь эмоций и соответствующих синонимов.
    :val emotion_vocab: Словарь эмоций и соответствующих слов.
    :val context_keywords: Список ключевых слов для анализа контекста.
    """

    emotion_synonyms: Dict[str, List[str]]
    emotion_vocab: Dict[str, List[str]]
    context_keywords: List[str]

    def __init__(
            self,
            emotion_synonyms_path: Path,
            emotion_vocab_path: Path,
            context_keywords: Optional[List[str]] = None
    ) -> None:
        """
        Инициализирует анализатор эмоций.

        :param emotion_synonyms_path: Путь к JSON-файлу с синонимами эмоций.
        :param emotion_vocab_path: Путь к JSON-файлу с вокабуляром эмоций.
        :param context_keywords: Список ключевых слов для анализа контекста.
        """
        self.emotion_synonyms = self._load_json(emotion_synonyms_path)
        self.emotion_vocab = self._load_json(emotion_vocab_path)
        self.context_keywords = context_keywords or [
            "Putin", "russischer Präsident", "Russland",
            "Moskau", "Russische Föderation", "Ukraine",
            "Krieg", "Auseinandersetzung"
        ]
        logger.info("EmotionAnalyzer инициализирован.")

    @staticmethod
    def _load_json(file_path: Path) -> Dict[str, List[str]]:
        """
        Загружает JSON-файл.

        :param file_path: Путь к JSON-файлу.
        :return: Словарь с данными из файла.
        """
        try:
            with file_path.open(encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Файл {file_path} успешно загружен.")
            return data
        except Exception as e:
            logger.error(f"Ошибка загрузки файла {file_path}: {e}")
            return {}

    async def analyze_emotions_in_texts(self, texts: List[str]) -> Dict[str, Any]:
        """
        Анализирует эмоции в предоставленных текстах.

        :param texts: Список текстов выступлений.
        :return: Результаты анализа.
        """
        emotion_counts = Counter()
        context_counts = Counter()

        for text in texts:
            words = text.split()
            for index, word in enumerate(words):
                for emotion, synonyms in self.emotion_synonyms.items():
                    if word.lower() in map(str.lower, synonyms):
                        emotion_counts[emotion] += 1
                        # Проверка контекста
                        start = max(index - 3, 0)
                        end = min(index + 4, len(words))
                        context = words[start:index] + words[index + 1:end]
                        if any(
                                kw.lower() in map(str.lower, context)
                                for kw in self.context_keywords
                        ):
                            context_counts[emotion] += 1
            await asyncio.sleep(0)  # Асинхронная совместимость

        logger.info("Анализ эмоций завершен.")
        return {
            "emotion_counts": dict(emotion_counts),
            "context_counts": dict(context_counts)
        }


class ModalParticleAnalyzer:
    """
    Класс для анализа модальных частиц в текстах выступлений.

    :val modal_particles: Список модальных частиц.
    """

    modal_particles: List[str]

    def __init__(self, modal_particles_path: Path) -> None:
        """
        Инициализирует анализатор модальных частиц.

        :param modal_particles_path: Путь к JSON-файлу с модальными частицами.
        """
        self.modal_particles = self._load_json(modal_particles_path)
        logger.info("ModalParticleAnalyzer инициализирован.")

    @staticmethod
    def _load_json(file_path: Path) -> List[str]:
        """
        Загружает JSON-файл с модальными частицами.

        :param file_path: Путь к JSON-файлу.
        :return: Список модальных частиц.
        """
        try:
            with file_path.open(encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Файл {file_path} успешно загружен.")
            return data
        except Exception as e:
            logger.error(f"Ошибка загрузки файла {file_path}: {e}")
            return []

    async def analyze_particles_frequency(self, texts: List[str]) -> Counter:
        """
        Анализирует частоту использования модальных частиц в текстах.

        :param texts: Список текстов выступлений.
        :return: Счётчик частотности модальных частиц.
        """
        particle_counter = Counter()
        for text in texts:
            words = text.split()
            for word in words:
                if word.lower() in map(str.lower, self.modal_particles):
                    particle_counter[word.lower()] += 1
            await asyncio.sleep(0)  # Асинхронная совместимость

        logger.info("Анализ модальных частиц завершен.")
        return particle_counter


class SpeechAnalyzer:
    """
    Главный класс для анализа текстов выступлений.

    :val emotion_analyzer: Экземпляр EmotionAnalyzer.
    :val particle_analyzer: Экземпляр ModalParticleAnalyzer.
    :val speeches: Список текстов выступлений.
    """

    emotion_analyzer: EmotionAnalyzer
    particle_analyzer: ModalParticleAnalyzer
    speeches: List[str]

    def __init__(
            self,
            speeches_path: Path,
            emotion_synonyms_path: Path,
            emotion_vocab_path: Path,
            modal_particles_path: Path
    ) -> None:
        """
        Инициализирует анализатор выступлений.

        :param speeches_path: Путь к файлу с текстами выступлений.
        :param emotion_synonyms_path: Путь к JSON-файлу с синонимами эмоций.
        :param emotion_vocab_path: Путь к JSON-файлу с вокабуляром эмоций.
        :param modal_particles_path: Путь к JSON-файлу с модальными частицами.
        """
        self.speeches = self._load_speeches(speeches_path)
        self.emotion_analyzer = EmotionAnalyzer(
            emotion_synonyms_path,
            emotion_vocab_path
        )
        self.particle_analyzer = ModalParticleAnalyzer(modal_particles_path)
        logger.info("SpeechAnalyzer инициализирован.")

    @staticmethod
    def _load_speeches(file_path: Path) -> List[str]:
        """
        Загружает тексты выступлений из файла.

        :param file_path: Путь к файлу с текстами.
        :return: Список текстов.
        """
        try:
            with file_path.open(encoding='utf-8') as f:
                texts = f.read().split('\n\n')  # Предполагается разделение абзацами
            logger.info(f"Файл {file_path} успешно загружен.")
            return texts
        except Exception as e:
            logger.error(f"Ошибка загрузки файла {file_path}: {e}")
            return []

    async def run_analysis(self) -> None:
        """
        Запускает весь процесс анализа.

        :return: None
        """
        emotion_results = await self.emotion_analyzer.analyze_emotions_in_texts(self.speeches)
        particle_counts = await self.particle_analyzer.analyze_particles_frequency(self.speeches)

        self._generate_emotion_report(emotion_results)
        self._generate_particle_graph(particle_counts)

    def _generate_emotion_report(self, results: Dict[str, Any]) -> None:
        """
        Генерирует и выводит отчет по эмоциям.

        :param results: Результаты анализа эмоций.
        :return: None
        """
        logger.info("Отчет по эмоциям:")
        logger.info(f"Количество эмоций: {results['emotion_counts']}")
        logger.info(f"Эмоции в контексте ключевых слов: {results['context_counts']}")

    def _generate_particle_graph(self, particle_counts: Counter) -> None:
        """
        Генерирует график частотности модальных частиц.

        :param particle_counts: Счётчик частотности модальных частиц.
        :return: None
        """
        particles, counts = zip(*particle_counts.items())
        plt.figure(figsize=(10, 6))
        plt.bar(particles, counts, color='skyblue')
        plt.xlabel('Модальные частицы')
        plt.ylabel('Частота использования')
        plt.title('Частотность модальных частиц в речах А. Меркель')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('modal_particles_frequency.png')
        plt.close()
        logger.info("График частотности модальных частиц сохранен как 'modal_particles_frequency.png'.")


async def main() -> None:
    """
    Главная асинхронная функция для запуска анализа.

    :return: None
    """
    analyzer = SpeechAnalyzer(
        speeches_path=Path(r'C:\Users\Client\Desktop\Влад\Send_message\am\pars\pages\bt.txt'),
        emotion_synonyms_path=Path('es.json'),
        emotion_vocab_path=Path('ev.json'),
        modal_particles_path=Path('mp.json')
    )
    await analyzer.run_analysis()


if __name__ == "__main__":
    asyncio.run(main())
