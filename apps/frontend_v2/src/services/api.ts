// Minimal API stubs. Replace with real endpoints when backend is available.
export async function fetchTasks(){
  return Promise.resolve([
    { id: '1', title: 'Design login screen', status: 'todo' },
    { id: '2', title: 'Implement API contract', status: 'in-progress' }
  ])
}

export async function fetchTask(id: string){
  return Promise.resolve({ id, title: `Task ${id}`, status: 'todo', description: '' })
}

export async function saveTask(payload: any){
  return Promise.resolve({ ok: true, id: 'new' })
}
