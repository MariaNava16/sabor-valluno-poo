from abc import ABC, abstractmethod


class Pago(ABC):
    def __init__(self, monto: float):
        if monto <= 0:
            raise ValueError("El monto del pago debe ser mayor a cero")
        self._monto = round(float(monto), 2)
        self._confirmado = False

    @property
    def monto(self) -> float:
        return self._monto

    @property
    def confirmado(self) -> bool:
        return self._confirmado

    def permite_delivery(self) -> bool:
        return True

    @abstractmethod
    def validar_pago(self) -> bool:
        pass

    def confirmar(self):
        if not self.validar_pago():
            raise ValueError("El pago no cumple con las condiciones de validación")
        self._confirmado = True


class Efectivo(Pago):
    def __init__(self, monto: float, monto_recibido: float):
        super().__init__(monto)
        self._monto_recibido = round(float(monto_recibido), 2)

    @property
    def monto_recibido(self) -> float:
        return self._monto_recibido

    def calcular_cambio(self) -> float:
        if self._monto_recibido < self._monto:
            raise ValueError("El efectivo recibido es insuficiente")
        return round(self._monto_recibido - self._monto, 2)

    def validar_pago(self) -> bool:
        return self._monto_recibido >= self._monto


class Qr(Pago):
    def __init__(self, monto: float, codigo_transferencia: str):
        super().__init__(monto)
        self._codigo_transferencia = codigo_transferencia.strip()

    @property
    def codigo_transferencia(self) -> str:
        return self._codigo_transferencia

    def validar_pago(self) -> bool:
        return len(self._codigo_transferencia) >= 4


class Tarjeta(Pago):
    COMISION = 0.0

    def __init__(self, monto: float, ultimos_digitos: str):
        super().__init__(monto)
        self._ultimos_digitos = ultimos_digitos.strip()

    def permite_delivery(self) -> bool:
        return False  # Variante A: Delivery solo acepta Efectivo o QR

    def calcular_comision(self) -> float:
        return round(self._monto * self.COMISION, 2)

    def validar_pago(self) -> bool:
        return len(self._ultimos_digitos) == 4 and self._ultimos_digitos.isdigit()