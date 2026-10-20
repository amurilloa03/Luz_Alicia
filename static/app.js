const formulario = document.getElementById("formulario-factura");
const panelResultado = document.getElementById("panel-resultado");
const resultadoCaja = document.getElementById("resultado-caja");
const btnEnviar = document.getElementById("btn-enviar");

const colores = {
  Bajo: "border-emerald-200 bg-emerald-50 text-emerald-900",
  Medio: "border-amber-200 bg-amber-50 text-amber-900",
  Alto: "border-rose-200 bg-rose-50 text-rose-900",
};

formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const datos = {
    titular: document.getElementById("titular").value,
    potencia_kw: parseFloat(document.getElementById("potencia").value),
    consumo_kwh: parseFloat(document.getElementById("consumo").value),
    dias: parseInt(document.getElementById("dias").value),
    discriminacion_horaria: document.getElementById("discriminacion").checked,
    bono_social: document.getElementById("bono").checked,
  };

  btnEnviar.disabled = true;
  btnEnviar.textContent = "Calculando...";

  try {
    const respuesta = await fetch("/api/calcular-factura", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos),
    });

    if (!respuesta.ok) {
      throw new Error(`Error en la API: ${respuesta.status}`);
    }

    const r = await respuesta.json();

    panelResultado.classList.remove("hidden");
    resultadoCaja.className = `p-6 rounded-xl border ${colores[r.nivel_consumo]}`;
    resultadoCaja.innerHTML = `
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-xl font-bold">Total: ${r.importe_total} €</h3>
        <span class="px-3 py-1 bg-white rounded-full font-bold text-sm">Consumo ${r.nivel_consumo}</span>
      </div>
      <p class="text-sm mb-1"><strong>Titular:</strong> ${r.titular}</p>
      <p class="text-sm mb-1"><strong>Consumo medio:</strong> ${r.consumo_medio_diario} kWh/día</p>
      <p class="text-sm mb-1"><strong>Término de potencia:</strong> ${r.termino_potencia} €</p>
      <p class="text-sm mb-1"><strong>Término de energía:</strong> ${r.termino_energia} €</p>
      <p class="text-sm mb-3"><strong>Impuestos (IE + IVA):</strong> ${r.impuestos} €</p>
      <p class="text-sm italic">${r.mensaje}</p>
    `;
  } catch (error) {
    alert("No se ha podido comunicar con la API. Comprueba que el servidor está en marcha.");
    console.error(error);
  } finally {
    btnEnviar.disabled = false;
    btnEnviar.textContent = "Calcular factura";
  }
});
