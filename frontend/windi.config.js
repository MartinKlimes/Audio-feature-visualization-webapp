export default {
    theme: {},
    
    shortcuts: 
    {
        
        'btn': 'py-1 px-2 text-sm rounded-md shadow-md h-7',
        'btn-hover': 'py-1 px-2 text-sm rounded-md shadow-md h-7  hover:bg-gray-300 transition',
        'btn-hover-cursor': 'text-sm rounded-md shadow- hover:bg-gray-300 transition cursor-pointer',
        'btn-blue': 'text-white bg-blue-800 hover:bg-blue-700 transition',
        'btn-dark': 'text-white bg-black hover:bg-dark-50 transition',
        'btn-disabled': 'text-white bg-dark-800 opacity-50 cursor-default',
        'btn-blue-border': 'text-white bg-blue-400 hover:bg-blue-700 transition',
        'btn-visualization': 'w-20 h-max p-0.5 text-sm text-xs border border-gray-700 rounded-md bg-blue-400 hover:bg-gray-300 duration-200',

        'input-field': 'h-7 mb-5 p-2 rounded-md text-black text-sm',
        'input-field-nomargin': 'h-7 p-2 rounded-md text-black text-sm',

        
    },
    
    plugins: [
        // require('windicss/plugin/forms'),
        require('windicss/plugin/filters'),
        require('@windicss/plugin-animations')({
            settings: {
              animatedSpeed: 1000,
              heartBeatSpeed: 1000,
              hingeSpeed: 2000,
              bounceInSpeed: 750,
              bounceOutSpeed: 750,
              animationDelaySpeed: 1000,
            },
          }),
    ]
  
}
  