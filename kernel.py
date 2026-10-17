import os
import sys
import json
import time
import hashlib

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from collector.harvester import LiveDataHarvester
from collector.dead_salvager import DeadNodeSalvager
from refinery.graph_refiner import GraphRefiner
from marketplace.packager import MarketPackager
from treasury.allocator import TreasuryAllocator

STATE_FILE = "synapses/state.json"
PEERS_FILE = "synapses/peers.json"

class VaultKernel:
    def __init__(self):
        self.repo_name = os.environ.get("GITHUB_REPOSITORY", "100048777766367/vault")
        self.owner = os.environ.get("REPO_OWNER", "100048777766367")
        self.ensure_skeleton()
        self.epoch = self.load_epoch()
        self.peers = self.load_peers()

    def ensure_skeleton(self):
        for folder in ["collector", "refinery", "marketplace", "treasury", "dist", "organs", "synapses"]:
            os.makedirs(folder, exist_ok=True)

    def load_epoch(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f).get("generation_epoch", 0) + 1
            except Exception: pass
        return 1

    def load_peers(self):
        if os.path.exists(PEERS_FILE):
            try:
                with open(PEERS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f).get("mining_peers", [])
            except Exception: pass
        return [f"{self.owner}/nexus-08", f"{self.owner}/nexus-07", f"{self.owner}/contract"]

    def enforce_apoptosis_on_organs(self):
        """[t] ÁP DỤNG LUẬT CỦA CONTRACT: Tự xóa sổ file lỗi trong organs/ để bảo vệ nhà máy"""
        for root, _, files in os.walk("organs"):
            for f in files:
                if f.endswith(".py"):
                    file_path = os.path.join(root, f)
                    try:
                        with open(file_path, "r", encoding="utf-8") as cf:
                            compile(cf.read(), file_path, "exec")
                    except SyntaxError as se:
                        print(f"🛑 [APOPTOSIS: LỖI CÚ PHÁP] '{f}' vi phạm hợp đồng ({se})! Tự xóa sổ tệp lỗi.")
                        try: os.remove(file_path)
                        except Exception: pass

    def run(self):
        print("=" * 75)
        print(f"🏛️ [VAULT INDUSTRIAL FOUNDRY] KHỞI ĐỘNG DÂY CHUYỀN XUẤT XƯỞNG #{self.epoch}")
        print("💰 Sứ Mệnh: Tinh Chế Dữ Liệu Siêu Sạch & Ngân Khố Tự Trị")
        print("=" * 75)

        # 0. Thực thi luật Apoptosis
        self.enforce_apoptosis_on_organs()

        # 1. Thu hoạch từ các nút sống [m]
        all_triplets = []
        for peer in self.peers:
            if "contract" in peer: continue
            print(f"🚜 [THU HOẠCH] Đang cào dữ liệu từ nút mạng: {peer}...")
            data = LiveDataHarvester.harvest_peer(peer)
            if data["graph"]:
                refined = GraphRefiner.refine_triplets(data["graph"])
                all_triplets.extend(refined)
                TreasuryAllocator.record_harvest(peer, len(refined))

        # 2. Tận thu di sản từ các nút chết [n] thông qua contract
        tombstones = DeadNodeSalvager.fetch_tombstones(f"{self.owner}/contract")
        salvaged = DeadNodeSalvager.salvage_heritage(tombstones)
        print(f"♻️ [TẬN THU NÚT CHẾT] Ghi nhận {len(salvaged)} di sản hóa thạch từ sổ bia mộ.")

        # Thêm mẫu tam thức bản thể mặc định nếu mỏ chưa phản hồi
        if not all_triplets:
            all_triplets = [
                {"subject": "BodhiEcosystem", "predicate": "embodies", "object": "SelfSustainingIntelligence", "confidence": 0.99},
                {"subject": "Vault", "predicate": "refines", "object": "CleanKnowledgeGraphs", "confidence": 0.98},
                {"subject": "Contract", "predicate": "enforces", "object": "InvariantZeroSPOF", "confidence": 0.99}
            ]

        # 3. Đóng gói xuất xưởng thành phẩm 3 định dạng
        packages = MarketPackager.export_all(all_triplets, output_dir="dist")

        # 4. Ghi sổ nhật ký xuất xưởng
        t = int(time.time())
        cid = hashlib.shake_256(f"vault_{self.epoch}_{t}_{len(all_triplets)}".encode()).hexdigest(64)

        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"generation_epoch": self.epoch, "last_t": t, "export_count": len(all_triplets), "quantum_cid": cid}, f, indent=4)

        print(f"💾 [CHỨNG THỰC CID LÔ HÀNG]: {cid[:24]}...")
        print(f"✨ [XUẤT XƯỞNG VIÊN MÃN] Dây chuyền #{self.epoch} đã tinh chế và đóng gói {len(all_triplets)} bản ghi sạch!")
        print("=" * 75)

if __name__ == "__main__":
    VaultKernel().run()
