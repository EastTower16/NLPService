import paddle.inference as paddle_infer
from langdetect import detect
from loguru import logger
from typing import List, Dict
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

class SentimentService:
    def __init__(self):
        self.cn_model = None
        self.en_model = None
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.model_path = os.getenv("MODEL_PATH", "models/senta")

    async def initialize(self):
        """Initialize Chinese and English models"""
        try:
            # Initialize Chinese model
            cn_config = paddle_infer.Config(
                os.path.join(self.model_path, "cn_model/model.pdmodel"),
                os.path.join(self.model_path, "cn_model/model.pdiparams")
            )
            self.cn_model = paddle_infer.create_predictor(cn_config)

            # Initialize English model
            en_config = paddle_infer.Config(
                os.path.join(self.model_path, "en_model/model.pdmodel"),
                os.path.join(self.model_path, "en_model/model.pdiparams")
            )
            self.en_model = paddle_infer.create_predictor(en_config)

            # Warmup models
            await self._warmup_models()
            logger.info("Models initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize models: {str(e)}")
            raise

    async def _warmup_models(self):
        """Warmup models with empty inference"""
        warmup_texts = ["测试文本", "test text"]
        for text in warmup_texts:
            await self.analyze(text)

    async def analyze(self, text: str) -> Dict:
        """Analyze sentiment for a single text"""
        try:
            # Detect language
            lang = detect(text)
            model = self.cn_model if lang == "zh" else self.en_model

            # Run inference in thread pool
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                self._predict,
                model,
                text
            )
            return result
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            raise

    async def batch_analyze(self, texts: List[str]) -> List[Dict]:
        """Analyze sentiment for multiple texts"""
        try:
            tasks = [self.analyze(text) for text in texts]
            results = await asyncio.gather(*tasks)
            return results
        except Exception as e:
            logger.error(f"Error in batch sentiment analysis: {str(e)}")
            raise

    def _predict(self, model: paddle_infer.Predictor, text: str) -> Dict:
        """Run model inference"""
        # TODO: Implement actual model inference logic
        # This is a placeholder that returns dummy results
        return {
            "label": "positive",
            "confidence": 0.95
        }

# Create global service instance
sentiment_service = SentimentService() 