import os
import shutil
import subprocess
import time

from jinja2 import Template
import glob

from datetime import datetime
from pydantic import UUID4
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


from app.repositories.trigger_repository import TriggerRepository
from app.repositories.controller_repository import ControllerRepository
from app.repositories.device_repository import DeviceRepository
from app.schemas.esp_schemas import TriggerValueOut, ControllerStateOut, TriggerValueIn
from app.schemas.trigger_schemas import Trigger


class EspService:
    def __init__(self, session: AsyncSession,
                 trigger_repository: TriggerRepository,
                 controller_repository: ControllerRepository,
                 device_repository: DeviceRepository):
        self.session = session
        self.trigger_repository = trigger_repository
        self.controller_repository = controller_repository
        self.device_repository = device_repository

        self.template_dir = "C:/Users/ashna/PycharmProjects/ControllerBackEnd/esp_firmware_template"

        self.builds_dir = "C:/Users/ashna/PycharmProjects/ControllerBackEnd/builds"
        os.makedirs(self.builds_dir, exist_ok=True)

    async def generate_firmware_for_device(self, device_id: UUID4):
        triggers = await self.trigger_repository.get_many_by(device_id=device_id)
        triggers_config = []

        for t in triggers:
            triggers_config.append({
                "id": str(t.id),
                "name": t.name,
                "type": t.type,
                "pin": t.pin
            })

        controllers = await self.controller_repository.get_many_by(device_id=device_id)
        controllers_config = []
        for c in controllers:
            controllers_config.append({
                "id": str(c.id),
                "name": c.name,
                "pin": c.pin,
            })

        template_path = os.path.join(self.template_dir, "template.cpp")
        main_cpp_path = os.path.join(self.template_dir, "src", "main.cpp")
        with open(template_path, "r", encoding="utf-8")as f:
            template_content = f.read()

        build_version = str(int(time.time()))  # Наприклад: "1748361234"

        template = Template(template_content)
        rendered_code = template.render(
            triggers=triggers_config,
            controllers=controllers_config,
            device_id=str(device_id),
            build_version=build_version
        )

        with open(main_cpp_path, "w", encoding="utf-8") as f:
            f.write(rendered_code)

        old_firmwares = glob.glob(os.path.join(self.builds_dir, f"{device_id}_*.bin"))
        for old_file in old_firmwares:
            try:
                os.remove(old_file)
                print(f"Видалено стару версію прошивки: {old_file}")
            except Exception as e:
                print(f"Не вдалося видалити файл {old_file}: {e}")
        # ----------------================================================-

        print(f"Початок прямої збірки прошивки для пристрою {device_id}...")

        pio_path = "C:/Users/ashna/.platformio/penv/Scripts/pio.exe"

        # 3. Запускаємо PlatformIO і компілюємо файл одразу в потрібне місце
        result = subprocess.run(
            [pio_path, "run", "-d", self.template_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )

        if result.returncode != 0:
            print("Помилка компіляції PlatformIO:", result.stderr)
            raise HTTPException(status_code=500, detail="PlatformIO compilation failed")

        compiled_bin_path = os.path.join(self.template_dir, ".pio", "build", "esp32doit-devkit-v1", "firmware.bin")

        if not os.path.exists(compiled_bin_path):
            raise HTTPException(status_code=500, detail="Compiled firmware.bin not found")

        target_bin_path = os.path.join(self.builds_dir, f"{device_id}_{build_version}.bin")
        shutil.copyfile(compiled_bin_path, target_bin_path)
        print(f"[SUCCESS] Нову прошивку скопійовано в: {target_bin_path}")

        # 6. ЕКОНОМІЯ ПАМ'ЯТІ: Видаляємо оригінальний firmware.bin з папки .pio,
        # щоб він не дублювався і не займав місце на сервері!
        try:
            os.remove(compiled_bin_path)
            print("[CLEANUP] Оригінальний файл firmware.bin у папці шаблону видалено.")
        except Exception as e:
            print(f"[CLEANUP] Не вдалося видалити оригінальний firmware.bin: {e}")

        return build_version


    async def update_last_val(self, trigger_id: UUID4, payload: TriggerValueIn) -> TriggerValueIn:
        try:
            trigger = await self.trigger_repository.get_one(id=trigger_id)
            trigger.last_value = payload.value
            await self.triggering(trigger)
            await self.session.commit()
            return TriggerValueIn.model_validate(payload)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Barabashka"
            )

    async def triggering(self, trigger: Trigger):
        controllers = await self.controller_repository.get_many_by(trigger_id=trigger.id)

        for controller in controllers:
            if not controller.is_automatic:
                continue

            if controller.trigger_vector is None:
                continue

            should_be_on = False
            if controller.trigger_vector == "<":
                if trigger.last_value < controller.trigger_value:
                    should_be_on = True

            elif controller.trigger_vector == ">":
                if trigger.last_value > controller.trigger_value:
                    should_be_on = True

            if controller.last_state != should_be_on:
                controller.last_state = should_be_on
                controller.updated_at = datetime.utcnow()




    async def get_controller_state(self, controller_id: UUID4) -> ControllerStateOut:
        controller = await self.controller_repository.get_one(id=controller_id)
        if not controller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Controller not found"
            )

        return ControllerStateOut(
            controller_id=controller.id,
            last_state=controller.last_state,
        )

    async def ping_device(self, device_id: UUID4) -> dict:
        device = await self.device_repository.get_one(id=device_id)
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )

        now = datetime.utcnow()
        await self.device_repository.update_one(
            {"last_seen": now},
            id=device_id
        )
        await self.session.commit()

        return {"device_id": str(device_id), "last_seen": str(now)}