import React, { createContext, useContext, useState } from 'react'

type StoreState = {
  user: { name: string } | null
  setUser: (u: any)=>void
}

const ctx = createContext<StoreState | undefined>(undefined)

export function StoreProvider({ children }: { children: React.ReactNode }){
  const [user, setUser] = useState<{name:string} | null>({ name: 'Demo User' })
  return <ctx.Provider value={{ user, setUser }}>{children}</ctx.Provider>
}

export function useStore(){
  const v = useContext(ctx)
  if(!v) throw new Error('useStore must be used inside StoreProvider')
  return v
}
