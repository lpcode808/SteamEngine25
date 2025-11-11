// Netlify Identity Authentication
// This script protects the site with Netlify Identity OAuth

declare global {
  interface Window {
    netlifyIdentity: {
      on: (event: string, callback: (user: any) => void) => void
      currentUser: () => any
      open: (tab?: string) => void
      close: () => void
    }
  }
}

// Check authentication status when page loads
document.addEventListener("DOMContentLoaded", () => {
  if (window.netlifyIdentity) {
    window.netlifyIdentity.on("init", (user) => {
      if (!user) {
        // User not logged in - show login modal
        window.netlifyIdentity.open("login")
      }
    })

    // Handle login success
    window.netlifyIdentity.on("login", () => {
      window.netlifyIdentity.close()
      // Refresh page to show authenticated content
      location.reload()
    })

    // Handle logout
    window.netlifyIdentity.on("logout", () => {
      // Redirect to login
      window.netlifyIdentity.open("login")
    })
  }
})
