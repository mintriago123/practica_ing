/** @type {import('next').NextConfig} */
const nextConfig = {
  // Si quieres ocultar los dev indicators:
  devIndicators: {
    buildActivity: false,
    buildActivityPosition: 'bottom-right'
  },
  typescript: {
    ignoreBuildErrors: true,
  }
}

module.exports = nextConfig