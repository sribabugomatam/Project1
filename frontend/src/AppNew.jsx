import { useEffect, useMemo, useState } from 'react'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

const emptyFlatForm = {
  flat_number: '',
  floor_number: '',
  status: 'Owner Occupied',
}

const emptyResidentForm = {
  flat_id: '',
  full_name: '',
  role: '',
  phone: '',
  email: '',
  is_primary_contact: true,
}

const emptyParkingForm = {
  spot_number: '',
  location: 'Ground Floor',
  assigned_flat_id: '',
  spot_type: 'Default',
}

function getViewFromHash() {
  const hash = window.location.hash.replace('#', '')
  return ['home', 'flats', 'residents', 'parking'].includes(hash) ? hash : 'home'
}

function App() {
  const [currentView, setCurrentView] = useState(getViewFromHash())
  const [flats, setFlats] = useState([])
  const [residents, setResidents] = useState([])
  const [parking, setParking] = useState([])
  const [health, setHealth] = useState('checking...')
  const [message, setMessage] = useState('')
  const [flatForm, setFlatForm] = useState(emptyFlatForm)
  const [residentForm, setResidentForm] = useState(emptyResidentForm)
  const [parkingForm, setParkingForm] = useState(emptyParkingForm)
  const [editingFlatId, setEditingFlatId] = useState(null)
  const [editingResidentId, setEditingResidentId] = useState(null)
  const [editingParkingId, setEditingParkingId] = useState(null)

  const residentsByFlat = useMemo(() => {
    return flats.reduce((acc, flat) => {
      acc[flat.id] = residents.filter((resident) => resident.flat_id === flat.id)
      return acc
    }, {})
  }, [flats, residents])

  const loadData = async () => {
    try {
      const [flatsRes, residentsRes, parkingRes] = await Promise.all([
        axios.get(`${API_BASE}/flats`),
        axios.get(`${API_BASE}/residents`),
        axios.get(`${API_BASE}/parking`),
      ])
      setFlats(flatsRes.data)
      setResidents(residentsRes.data)
      setParking(parkingRes.data)
      setHealth('ok')
    } catch (error) {
      setHealth('backend unavailable')
      setMessage('Unable to load data from the backend.')
    }
  }

  useEffect(() => {
    const handleHashChange = () => setCurrentView(getViewFromHash())
    window.addEventListener('hashchange', handleHashChange)

    axios.get(`${API_BASE}/health`)
      .then((response) => setHealth(response.data.status))
      .catch(() => setHealth('backend unavailable'))

    loadData()

    return () => window.removeEventListener('hashchange', handleHashChange)
  }, [])

  const navigate = (view) => {
    window.location.hash = view
    setCurrentView(view)
  }

  const handleFlatSubmit = async (event) => {
    event.preventDefault()
    try {
      const payload = {
        ...flatForm,
        floor_number: Number(flatForm.floor_number),
      }
      if (editingFlatId) {
        await axios.put(`${API_BASE}/flats/${editingFlatId}`, payload)
        setMessage('Flat updated successfully.')
      } else {
        await axios.post(`${API_BASE}/flats`, payload)
        setMessage('Flat created successfully.')
      }
      setFlatForm(emptyFlatForm)
      setEditingFlatId(null)
      loadData()
    } catch (error) {
      setMessage('Failed to save flat.')
    }
  }

  const startFlatEdit = (flat) => {
    setEditingFlatId(flat.id)
    setFlatForm({
      flat_number: flat.flat_number,
      floor_number: flat.floor_number,
      status: flat.status,
    })
    navigate('flats')
  }

  const handleFlatDelete = async (flatId) => {
    try {
      await axios.delete(`${API_BASE}/flats/${flatId}`)
      setMessage('Flat deleted successfully.')
      loadData()
    } catch (error) {
      setMessage('Failed to delete flat.')
    }
  }

  const handleResidentSubmit = async (event) => {
    event.preventDefault()
    try {
      const payload = {
        ...residentForm,
        flat_id: Number(residentForm.flat_id),
        is_primary_contact: Boolean(residentForm.is_primary_contact),
      }
      if (editingResidentId) {
        await axios.put(`${API_BASE}/residents/${editingResidentId}`, payload)
        setMessage('Resident updated successfully.')
      } else {
        await axios.post(`${API_BASE}/residents`, payload)
        setMessage('Resident created successfully.')
      }
      setResidentForm(emptyResidentForm)
      setEditingResidentId(null)
      loadData()
    } catch (error) {
      setMessage('Failed to save resident.')
    }
  }

  const startResidentEdit = (resident) => {
    setEditingResidentId(resident.id)
    setResidentForm({
      flat_id: resident.flat_id,
      full_name: resident.full_name,
      role: resident.role,
      phone: resident.phone || '',
      email: resident.email || '',
      is_primary_contact: resident.is_primary_contact,
    })
    navigate('residents')
  }

  const handleResidentDelete = async (residentId) => {
    try {
      await axios.delete(`${API_BASE}/residents/${residentId}`)
      setMessage('Resident deleted successfully.')
      loadData()
    } catch (error) {
      setMessage('Failed to delete resident.')
    }
  }

  const handleParkingSubmit = async (event) => {
    event.preventDefault()
    try {
      const payload = {
        ...parkingForm,
        assigned_flat_id: parkingForm.assigned_flat_id ? Number(parkingForm.assigned_flat_id) : null,
      }
      if (editingParkingId) {
        await axios.put(`${API_BASE}/parking/${editingParkingId}`, payload)
        setMessage('Parking spot updated successfully.')
      } else {
        await axios.post(`${API_BASE}/parking`, payload)
        setMessage('Parking spot created successfully.')
      }
      setParkingForm(emptyParkingForm)
      setEditingParkingId(null)
      loadData()
    } catch (error) {
      setMessage('Failed to save parking spot.')
    }
  }

  const startParkingEdit = (spot) => {
    setEditingParkingId(spot.id)
    setParkingForm({
      spot_number: spot.spot_number,
      location: spot.location,
      assigned_flat_id: spot.assigned_flat_id || '',
      spot_type: spot.spot_type,
    })
    navigate('parking')
  }

  const handleParkingDelete = async (spotId) => {
    try {
      await axios.delete(`${API_BASE}/parking/${spotId}`)
      setMessage('Parking spot deleted successfully.')
      loadData()
    } catch (error) {
      setMessage('Failed to delete parking spot.')
    }
  }

  const renderNav = () => (
    <nav className="flex flex-wrap items-center gap-2 rounded-2xl border border-slate-200 bg-white p-3 shadow-sm">
      <button onClick={() => navigate('home')} className={`rounded-lg px-3 py-2 text-sm font-medium ${currentView === 'home' ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-700'}`}>
        Home
      </button>
      <button onClick={() => navigate('flats')} className={`rounded-lg px-3 py-2 text-sm font-medium ${currentView === 'flats' ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-700'}`}>
        Flats
      </button>
      <button onClick={() => navigate('residents')} className={`rounded-lg px-3 py-2 text-sm font-medium ${currentView === 'residents' ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-700'}`}>
        Residents
      </button>
      <button onClick={() => navigate('parking')} className={`rounded-lg px-3 py-2 text-sm font-medium ${currentView === 'parking' ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-700'}`}>
        Parking
      </button>
    </nav>
  )

  return (
    <div className="min-h-screen bg-slate-100 p-4 text-slate-800 md:p-8">
      <div className="mx-auto max-w-6xl rounded-3xl bg-white p-6 shadow-xl md:p-8">
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Apartment HOA</p>
            <h1 className="mt-1 text-3xl font-semibold">Manage flats, residents, and parking in one place</h1>
            <p className="mt-2 max-w-2xl text-sm text-slate-600">Start with your flat list, add residents from scratch, and keep parking assignments aligned with each home.</p>
          </div>
          <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700">
            <span className="font-medium">Backend:</span> {health}
          </div>
        </div>

        <div className="mt-6">{renderNav()}</div>

        {message ? <div className="mt-4 rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700">{message}</div> : null}

        {currentView === 'home' && (
          <div className="mt-8 grid gap-4 md:grid-cols-3">
            <button onClick={() => navigate('flats')} className="rounded-2xl border border-slate-200 bg-slate-50 p-5 text-left transition hover:border-slate-400 hover:bg-white">
              <p className="text-lg font-semibold">Flats</p>
              <p className="mt-2 text-sm text-slate-600">Create or edit flat records and view who lives there.</p>
            </button>
            <button onClick={() => navigate('residents')} className="rounded-2xl border border-slate-200 bg-slate-50 p-5 text-left transition hover:border-slate-400 hover:bg-white">
              <p className="text-lg font-semibold">Residents</p>
              <p className="mt-2 text-sm text-slate-600">Add residents from scratch and link them to a flat.</p>
            </button>
            <button onClick={() => navigate('parking')} className="rounded-2xl border border-slate-200 bg-slate-50 p-5 text-left transition hover:border-slate-400 hover:bg-white">
              <p className="text-lg font-semibold">Parking</p>
              <p className="mt-2 text-sm text-slate-600">Track default spots and extra purchased spots in the ground floor and cellar.</p>
            </button>
          </div>
        )}

        {currentView === 'flats' && (
          <div className="mt-8 grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
            <section className="rounded-2xl border border-slate-200 p-5">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold">Flat records</h2>
                <span className="text-sm text-slate-500">Flat numbers use the floor + two-digit format such as 101 or 504.</span>
              </div>
              <form onSubmit={handleFlatSubmit} className="mt-4 space-y-3">
                <input className="w-full rounded-xl border border-slate-300 px-3 py-2" placeholder="Flat number" value={flatForm.flat_number} onChange={(e) => setFlatForm({ ...flatForm, flat_number: e.target.value })} />
                <input className="w-full rounded-xl border border-slate-300 px-3 py-2" type="number" placeholder="Floor number" value={flatForm.floor_number} onChange={(e) => setFlatForm({ ...flatForm, floor_number: e.target.value })} />
                <select className="w-full rounded-xl border border-slate-300 px-3 py-2" value={flatForm.status} onChange={(e) => setFlatForm({ ...flatForm, status: e.target.value })}>
                  <option>Owner Occupied</option>
                  <option>Rented</option>
                  <option>Vacant</option>
                </select>
                <button className="rounded-xl bg-slate-900 px-4 py-2 text-white" type="submit">{editingFlatId ? 'Update flat' : 'Add flat'}</button>
              </form>
              <div className="mt-6 space-y-3">
                {flats.map((flat) => (
                  <div key={flat.id} className="rounded-2xl border border-slate-200 p-3">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <p className="font-semibold">{flat.flat_number}</p>
                        <p className="text-sm text-slate-600">Floor {flat.floor_number} • {flat.status}</p>
                      </div>
                      <div className="flex gap-2 text-sm">
                        <button className="text-blue-600" onClick={() => startFlatEdit(flat)}>Edit</button>
                        <button className="text-red-600" onClick={() => handleFlatDelete(flat.id)}>Delete</button>
                      </div>
                    </div>
                    <div className="mt-3 rounded-xl bg-slate-50 p-3">
                      <p className="text-sm font-medium text-slate-700">Residents in this flat</p>
                      {residentsByFlat[flat.id]?.length ? (
                        <ul className="mt-2 space-y-1 text-sm text-slate-600">
                          {residentsByFlat[flat.id].map((resident) => <li key={resident.id}>• {resident.full_name} — {resident.role}</li>)}
                        </ul>
                      ) : <p className="mt-2 text-sm text-slate-500">No residents attached yet.</p>}
                    </div>
                  </div>
                ))}
              </div>
            </section>

            <aside className="rounded-2xl border border-slate-200 p-5">
              <h2 className="text-xl font-semibold">Add a resident to a flat</h2>
              <p className="mt-2 text-sm text-slate-600">You can create residents from scratch and connect them here.</p>
              <form onSubmit={handleResidentSubmit} className="mt-4 space-y-3">
                <select className="w-full rounded-xl border border-slate-300 px-3 py-2" value={residentForm.flat_id} onChange={(e) => setResidentForm({ ...residentForm, flat_id: e.target.value })}>
                  <option value="">Select flat</option>
                  {flats.map((flat) => <option key={flat.id} value={flat.id}>{flat.flat_number}</option>)}
                </select>
                <input className="w-full rounded-xl border border-slate-300 px-3 py-2" placeholder="Full name" value={residentForm.full_name} onChange={(e) => setResidentForm({ ...residentForm, full_name: e.target.value })} />
                <input className="w-full rounded-xl border border-slate-300 px-3 py-2" placeholder="Role" value={residentForm.role} onChange={(e) => setResidentForm({ ...residentForm, role: e.target.value })} />
                <input className="w-full rounded-xl border border-slate-300 px-3 py-2" placeholder="Phone" value={residentForm.phone} onChange={(e) => setResidentForm({ ...residentForm, phone: e.target.value })} />
                <input className="w-full rounded-xl border border-slate-300 px-3 py-2" placeholder="Email" value={residentForm.email} onChange={(e) => setResidentForm({ ...residentForm, email: e.target.value })} />
                <label className="flex items-center gap-2 text-sm text-slate-600">
                  <input type="checkbox" checked={residentForm.is_primary_contact} onChange={(e) => setResidentForm({ ...residentForm, is_primary_contact: e.target.checked })} />
                  Primary contact
                </label>
                <button className="rounded-xl bg-slate-900 px-4 py-2 text-white" type="submit">{editingResidentId ? 'Update resident' : 'Add resident'}</button>
              </form>
            </aside>
          </div>
        )}

        {currentView === 'residents' && (
          <div className="mt-8 grid gap-6 lg:grid-cols-[1fr_0.9fr]">
            <section className="rounded-2xl border border-slate-200 p-5">
              <h2 className="text-xl font-semibold">Resident list</h2>
              <div className="mt-4 space-y-3">
                {residents.length ? residents.map((resident) => (
                  <div key={resident.id} className="rounded-2xl border border-slate-200 p-3">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <p className="font-semibold">{resident.full_name}</p>
                        <p className="text-sm text-slate-600">{resident.role} • Flat {resident.flat_id}</p>
                        <p className="text-sm text-slate-500">{resident.phone || 'No phone'} • {resident.email || 'No email'}</p>
                      </div>
                      <div className="flex gap-2 text-sm">
                        <button className="text-blue-600" onClick={() => startResidentEdit(resident)}>Edit</button>
                        <button className="text-red-600" onClick={() => handleResidentDelete(resident.id)}>Delete</button>
                      </div>
                    </div>
                  </div>
                )) : <p className="text-sm text-slate-500">No residents added yet.</p>}
              </div>
            </section>

            <aside className="rounded-2xl border border-slate-200 p-5">
              <h2 className="text-xl font-semibold">Resident details</h2>
              <form onSubmit={handleResidentSubmit} className="mt-4 space-y-3">
                <select className="w-full rounded-xl border border-slate-300 px-3 py-2" value={residentForm.flat_id} onChange={(e) => setResidentForm({ ...residentForm, flat_id: e.target.value })}>
                  <option value="">Select flat</option>
                  {flats.map((flat) => <option key={flat.id} value={flat.id}>{flat.flat_number}</option>)}
                </select>
                <input className="w-full rounded-xl border border-slate-300 px-3 py-2" placeholder="Full name" value={residentForm.full_name} onChange={(e) => setResidentForm({ ...residentForm, full_name: e.target.value })} />
                <input className="w-full rounded-xl border border-slate-300 px-3 py-2" placeholder="Role" value={residentForm.role} onChange={(e) => setResidentForm({ ...residentForm, role: e.target.value })} />
                <input className="w-full rounded-xl border border-slate-300 px-3 py-2" placeholder="Phone" value={residentForm.phone} onChange={(e) => setResidentForm({ ...residentForm, phone: e.target.value })} />
                <input className="w-full rounded-xl border border-slate-300 px-3 py-2" placeholder="Email" value={residentForm.email} onChange={(e) => setResidentForm({ ...residentForm, email: e.target.value })} />
                <label className="flex items-center gap-2 text-sm text-slate-600">
                  <input type="checkbox" checked={residentForm.is_primary_contact} onChange={(e) => setResidentForm({ ...residentForm, is_primary_contact: e.target.checked })} />
                  Primary contact
                </label>
                <button className="rounded-xl bg-slate-900 px-4 py-2 text-white" type="submit">{editingResidentId ? 'Update resident' : 'Add resident'}</button>
              </form>
            </aside>
          </div>
        )}

        {currentView === 'parking' && (
          <div className="mt-8 grid gap-6 lg:grid-cols-[1fr_0.9fr]">
            <section className="rounded-2xl border border-slate-200 p-5">
              <h2 className="text-xl font-semibold">Parking spots</h2>
              <div className="mt-4 space-y-3">
                {parking.map((spot) => (
                  <div key={spot.id} className="rounded-2xl border border-slate-200 p-3">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <p className="font-semibold">{spot.spot_number}</p>
                        <p className="text-sm text-slate-600">{spot.location} • {spot.spot_type}</p>
                        <p className="text-sm text-slate-500">Assigned flat: {spot.assigned_flat_id ? flats.find((flat) => flat.id === spot.assigned_flat_id)?.flat_number || spot.assigned_flat_id : 'Unassigned'}</p>
                      </div>
                      <div className="flex gap-2 text-sm">
                        <button className="text-blue-600" onClick={() => startParkingEdit(spot)}>Edit</button>
                        <button className="text-red-600" onClick={() => handleParkingDelete(spot.id)}>Delete</button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            <aside className="rounded-2xl border border-slate-200 p-5">
              <h2 className="text-xl font-semibold">Parking details</h2>
              <form onSubmit={handleParkingSubmit} className="mt-4 space-y-3">
                <input className="w-full rounded-xl border border-slate-300 px-3 py-2" placeholder="Spot number (example: 101 or GF-01)" value={parkingForm.spot_number} onChange={(e) => setParkingForm({ ...parkingForm, spot_number: e.target.value })} />
                <select className="w-full rounded-xl border border-slate-300 px-3 py-2" value={parkingForm.location} onChange={(e) => setParkingForm({ ...parkingForm, location: e.target.value })}>
                  <option>Ground Floor</option>
                  <option>Underground Cellar</option>
                </select>
                <select className="w-full rounded-xl border border-slate-300 px-3 py-2" value={parkingForm.assigned_flat_id} onChange={(e) => setParkingForm({ ...parkingForm, assigned_flat_id: e.target.value })}>
                  <option value="">Unassigned</option>
                  {flats.map((flat) => <option key={flat.id} value={flat.id}>{flat.flat_number}</option>)}
                </select>
                <select className="w-full rounded-xl border border-slate-300 px-3 py-2" value={parkingForm.spot_type} onChange={(e) => setParkingForm({ ...parkingForm, spot_type: e.target.value })}>
                  <option>Default</option>
                  <option>Purchased Extra</option>
                </select>
                <button className="rounded-xl bg-slate-900 px-4 py-2 text-white" type="submit">{editingParkingId ? 'Update spot' : 'Add spot'}</button>
              </form>
            </aside>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
