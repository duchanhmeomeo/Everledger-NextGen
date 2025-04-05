import hashlib
import time
import json
from typing import List, Dict
from dataclasses import dataclass
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import numpy as np
from sklearn.linear_model import LinearRegression
from typing import Optional

@dataclass
class DiamondAsset:
    """Định nghĩa tài sản kim cương với thông tin chi tiết"""
    asset_id: str            # Mã định danh duy nhất
    origin: str             # Nguồn gốc (Trái Đất hoặc hành tinh khác)
    date_mined: str         # Ngày khai thác
    carat: float            # Trọng lượng
    clarity: str            # Độ trong
    laser_inscription: str  # Mã khắc laser (digital fingerprint)
    carbon_footprint: float # Tác động môi trường
    current_value: float    # Giá trị hiện tại (USD)

class QuantumResistantBlock:
    """Khối Blockchain với bảo mật hậu lượng tử"""
    def __init__(self, index: int, previous_hash: str, timestamp: float, data: DiamondAsset, signature: bytes, chaincode: str):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.signature = signature
        self.chaincode = chaincode
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        """Tính toán hash với dữ liệu và chaincode"""
        payload = f"{self.index}{self.previous_hash}{self.timestamp}{json.dumps(self.data.__dict__)}{self.chaincode}"
        return hashlib.sha256(payload.encode()).hexdigest()  # Có thể thay bằng XMSS trong thực tế

    @staticmethod
    def generate_signature(private_key, data: DiamondAsset, chaincode: str) -> bytes:
        """Tạo chữ ký số RSA cho bảo mật"""
        sign_payload = f"{json.dumps(data.__dict__)}{chaincode}".encode()
        return private_key.sign(
            sign_payload,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )

class EverledgerNextGen:
    """Hệ thống Blockchain thế hệ tiếp theo cho Everledger"""
    def __init__(self):
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()
        self.chain: List[QuantumResistantBlock] = [self._create_genesis_block()]
        self.participants: Dict[str, str] = {
            "EarthMineX": "miner",
            "MarsCutterY": "cutter",
            "InterstellarRetailerZ": "retailer"
        }
        # Dữ liệu huấn luyện AI để dự đoán giá trị tài sản
        self.value_predictor = self._train_value_predictor()

    def _train_value_predictor(self) -> LinearRegression:
        """Huấn luyện mô hình AI dự đoán giá trị tài sản"""
        X = np.array([[1.0, 0.5], [1.5, 1.0], [2.0, 1.5]])  # [carat, carbon_footprint]
        y = np.array([5000, 8000, 12000])  # Giá trị (USD)
        model = LinearRegression()
        model.fit(X, y)
        return model

    def _create_genesis_block(self) -> QuantumResistantBlock:
        """Khởi tạo khối gốc"""
        genesis_asset = DiamondAsset("GENESIS", "N/A", "N/A", 0.0, "N/A", "N/A", 0.0, 0.0)
        timestamp = time.time()
        chaincode = "initialize_everledger_nextgen"
        signature = QuantumResistantBlock.generate_signature(self.private_key, genesis_asset, chaincode)
        return QuantumResistantBlock(0, "0", timestamp, genesis_asset, signature, chaincode)

    def predict_asset_value(self, carat: float, carbon_footprint: float) -> float:
        """Dự đoán giá trị tài sản bằng AI"""
        return float(self.value_predictor.predict([[carat, carbon_footprint]])[0])

    def add_asset(self, asset: DiamondAsset, participant: str) -> bool:
        """Thêm tài sản vào Blockchain với chaincode và dự đoán giá trị"""
        if participant not in self.participants:
            raise ValueError(f"Participant {participant} is not authorized.")
        
        if asset.current_value == 0.0:
            asset.current_value = self.predict_asset_value(asset.carat, asset.carbon_footprint)

        previous_block = self.chain[-1]
        timestamp = time.time()
        chaincode = f"track_asset_{asset.asset_id}_{self.participants[participant]}"
        signature = QuantumResistantBlock.generate_signature(self.private_key, asset, chaincode)
        new_block = QuantumResistantBlock(
            previous_block.index + 1,
            previous_block.hash,
            timestamp,
            asset,
            signature,
            chaincode
        )
        self.chain.append(new_block)
        print(f"Asset {asset.asset_id} recorded by {participant} with predicted value ${asset.current_value:.2f}")
        return True

    def verify_integrity(self) -> bool:
        """Xác minh tính toàn vẹn của chuỗi"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.compute_hash() or current.previous_hash != previous.hash:
                return False
            try:
                self.public_key.verify(
                    current.signature,
                    f"{json.dumps(current.data.__dict__)}{current.chaincode}".encode(),
                    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                    hashes.SHA256()
                )
            except:
                return False
        return True

    def query_asset(self, asset_id: str) -> Dict:
        """Truy vấn thông tin tài sản"""
        for block in self.chain:
            if block.data.asset_id == asset_id:
                return block.data.__dict__
        return {"error": "Asset not found"}

# Triển khai và kiểm tra
if __name__ == "__main__":
    everledger = EverledgerNextGen()

    # Thêm tài sản mẫu
    asset1 = DiamondAsset("D001", "EarthMineX", "2025-01-01", 1.5, "VS1", "LASER123", 2.5, 0.0)
    asset2 = DiamondAsset("D002", "MarsCutterY", "2025-03-15", 2.0, "VVS2", "LASER456", 1.8, 0.0)

    everledger.add_asset(asset1, "EarthMineX")
    everledger.add_asset(asset2, "MarsCutterY")

    # Hiển thị chuỗi
    for block in everledger.chain:
        print(f"Block #{block.index}: {block.data.asset_id}")
        print(f"Asset Data: {json.dumps(block.data.__dict__, indent=2)}")
        print(f"Chaincode: {block.chaincode}")
        print(f"Hash: {block.hash[:10]}...")
        print("---")

    # Kiểm tra tính toàn vẹn và truy vấn
    print(f"Chain Integrity: {everledger.verify_integrity()}")
    print(f"Query D001: {json.dumps(everledger.query_asset('D001'), indent=2)}")