import type { Metadata } from 'next'
import './globals.css'
import AuthProviderWrapper from '@/components/AuthProviderWrapper'
import QueryProvider from '@/components/QueryProvider'

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
      <body>
        <QueryProvider>
          <AuthProviderWrapper>{children}</AuthProviderWrapper>
        </QueryProvider>
      </body>
    </html>
  )
}
