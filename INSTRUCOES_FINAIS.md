# Instruções Finais para Habilitar o Portal do Cliente

Olá!

A aplicação está pronta, mas o erro "Erro ao processar solicitação" que você está vendo é uma medida de segurança do seu banco de dados (Firestore) que precisa de uma pequena configuração para ser resolvida.

Por padrão, o Firestore не permite que visitantes anônimos (seus clientes) salvem dados. Para autorizar que eles enviem propostas, você precisa ajustar as **Regras de Segurança**.

## Passos para a Correção (Rápido e Simples)

1.  **Acesse o seu projeto no [Firebase Console](https://console.firebase.google.com/).**
2.  No menu à esquerda, navegue para **Build > Firestore Database**.
3.  No topo da página, clique na aba **Regras (Rules)**.
4.  Apague todo o conteúdo que está lá e cole o seguinte código:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Vendedores (autenticados) podem ler e escrever seus próprios dados.
    match /artifacts/{appId}/users/{userId}/{document=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }

    // Todos (incluindo clientes) podem ler a configuração pública da aplicação.
    match /artifacts/{appId}/public/data/appConfig/main {
      allow get: if true;
    }

    // Clientes (não autenticados) podem CRIAR propostas e clientes na coleção pública.
    match /publicArtifacts/{appId}/{document=**} {
      allow create: if true;
      // Vendedores (autenticados) podem LER as propostas enviadas pelos clientes.
      allow read: if request.auth != null;
    }

    // Clientes (não autenticados) podem adicionar e-mails na fila de envio.
    match /mail_queue/{mailId} {
      allow create: if true;
    }
  }
}
```

5.  Clique em **Publicar (Publish)**.

Após publicar estas regras, o sistema de envio de propostas para clientes funcionará perfeitamente.

Qualquer dúvida, estou à disposição.
