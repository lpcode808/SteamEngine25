import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import netlifyAuthScript from "./scripts/netlify-auth.inline"

// Component to handle Netlify Identity authentication
export default (() => {
  const NetlifyAuth: QuartzComponent = ({ displayClass }: QuartzComponentProps) => {
    return (
      <>
        <script>{netlifyAuthScript}</script>
        <div id="netlify-identity-container" className={displayClass}></div>
      </>
    )
  }

  NetlifyAuth.beforeDOMLoaded = netlifyAuthScript

  return NetlifyAuth
}) satisfies QuartzComponentConstructor
