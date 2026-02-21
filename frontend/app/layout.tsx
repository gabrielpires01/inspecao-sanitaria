import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Inspeção Sanitária',
  description: 'Sistema de gestão de inspeções sanitárias',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  )
}
