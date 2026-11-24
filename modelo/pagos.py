from abc import ABC, abstractmethod


class Pago(ABC):
    def __init__(self, monto, tipo):
        self.monto = monto
        self.tipo = tipo

    @property
    def monto(self):
        return self._monto

    @monto.setter
    def monto(self, monto):
        if monto <= 0:
            raise ValueError("El monto del pago debe ser mayor que cero.")
        self._monto = round(float(monto), 2)

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo):
        tipo_norm = tipo.strip().lower()
        if tipo_norm not in ["efectivo", "qr", "tarjeta"]:
            raise ValueError("Tipo de pago inválido. Debe ser efectivo, qr o tarjeta.")
        self.__tipo = tipo_norm

    @abstractmethod
    def validar_pago(self):
        pass


class Efectivo(Pago):
    def __init__(self, monto, monto_recibido):
        super().__init__(monto, "efectivo")
        self.monto_recibido = monto_recibido

    @property
    def monto_recibido(self):
        return self.__monto_recibido

    @monto_recibido.setter
    def monto_recibido(self, monto_recibido):
        if monto_recibido < self._monto:
            raise ValueError("Monto insuficiente. Debe cubrir el total del pedido.")
        self.__monto_recibido = round(float(monto_recibido), 2)

    def calcular_cambio(self):
        return round(self.__monto_recibido - self._monto, 2)

    def validar_pago(self):
        return self.__monto_recibido >= self._monto


class Qr(Pago):
    def __init__(self, monto, codigo_transaccion):
        super().__init__(monto, "qr")
        self.codigo_transaccion = codigo_transaccion

    @property
    def codigo_transaccion(self):
        return self.__codigo_transaccion

    @codigo_transaccion.setter
    def codigo_transaccion(self, codigo_transaccion):
        codigo = str(codigo_transaccion).strip()
        if not (codigo.isdigit() and len(codigo) == 10):
            raise ValueError("El código de transacción QR debe tener exactamente 10 dígitos.")
        self.__codigo_transaccion = codigo

    def validar_pago(self):
        return self.__codigo_transaccion.isdigit() and len(self.__codigo_transaccion) == 10


class Tarjeta(Pago):
    def __init__(self, monto):
        super().__init__(monto, "tarjeta")

    def calcular_comision(self):
        return round(self._monto * 0.03, 2)

    def calcular_total_con_comision(self):
        return round(self._monto + self.calcular_comision(), 2)

    def validar_pago(self):
        return self._monto > 0