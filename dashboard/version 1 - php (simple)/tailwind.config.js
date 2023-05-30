module.exports = {
  content: ['./src/**/*.{html,js}', './node_modules/tw-elements/dist/js/**/*.js'],
  plugins: [
    require('tw-elements/dist/plugin'),
    require('flowbite/plugin')
  ],
  theme: {
    screen: {
      sm: '480px',
      md: '768px',
      lg: '976px',
      xl: '1440px',
    },
    extend: {
      colors: {
        wBrown: 'rgba(83,46,31,255)',
        wYellow: 'rgba(241,196,0,255)',
        dBackground: 'rgba(31,33,40,255)',
        dCard: 'rgba(36,39,49,255)',
        dAccent: 'rgba(108,93,211,255)',


      },
    },
  },
}