import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [menu, setMenu] = useState([])
  const [carrito, setCarrito] = useState([])
  const [mensaje, setMensaje] = useState('')
  
  // ID del restaurante simulado
  const RESTAURANTE_ID = "restaurante-1" 
  const MESA_ID = "mesa-5"

  // 1. Cargar Menú desde el Microservicio de MENÚS (8001)
  useEffect(() => {
    const fetchMenu = async () => {
      try {
        // NOTA: Asegúrate que svc-menus esté corriendo
        const response = await axios.get(`http://127.0.0.1:8001/menus/${RESTAURANTE_ID}`)
        setMenu(response.data)
      } catch (error) {
        console.error("Error cargando menú:", error)
      }
    }
    fetchMenu()
  }, [])

  // 2. Función para agregar al carrito
  const agregarAlCarrito = (plato) => {
    setCarrito([...carrito, plato])
  }

  // 3. Enviar Pedido al Microservicio de PEDIDOS (8002)
  const realizarPedido = async () => {
    if (carrito.length === 0) return

    const total = carrito.reduce((sum, item) => sum + item.precio, 0)

    try {
      await axios.post('http://127.0.0.1:8002/pedidos/', {
        mesa_qr_id: MESA_ID,
        total: total
      })
      
      setMensaje(`¡Pedido enviado a cocina! ID Transacción: ${Date.now()}`)
      setCarrito([]) // Limpiar carrito
      
      // Ocultar mensaje a los 3 segundos
      setTimeout(() => setMensaje(''), 3000)

    } catch (error) {
      alert("Error al procesar el pedido. Intenta nuevamente.")
      console.error(error)
    }
  }

  return (
    <div className="container">
      <h1>🍔 SmartDine - {RESTAURANTE_ID}</h1>
      
      {mensaje && <div className="alert success">{mensaje}</div>}

      <div className="menu-grid">
        {/* Listado de Platos */}
        <div className="platos-section">
          <h2>Menú</h2>
          {menu.length === 0 ? <p>Cargando menú...</p> : null}
          
          {menu.map((plato) => (
            <div key={plato._id} className="card">
              <h3>{plato.nombre}</h3>
              <p>{plato.descripcion}</p>
              <div className="price-row">
                <span className="price">${plato.precio}</span>
                <button onClick={() => agregarAlCarrito(plato)}>Agregar +</button>
              </div>
            </div>
          ))}
        </div>

        {/* Carrito Lateral */}
        <div className="carrito-section">
          <h2>Tu Orden ({MESA_ID})</h2>
          <ul>
            {carrito.map((item, index) => (
              <li key={index}>{item.nombre} - ${item.precio}</li>
            ))}
          </ul>
          <div className="total">
            Total: ${carrito.reduce((sum, item) => sum + item.precio, 0)}
          </div>
          <button 
            className="btn-pagar" 
            disabled={carrito.length === 0}
            onClick={realizarPedido}
          >
            Confirmar Pedido
          </button>
        </div>
      </div>
    </div>
  )
}

export default App