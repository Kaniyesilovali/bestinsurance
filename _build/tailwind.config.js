/* Tailwind derleme yapılandırması.
   Bu klasör siteye YÜKLENMEZ — yalnızca CSS'i yeniden üretmek için.

   Sınıflar artık şablonlarda ve content/ içinde yaşıyor; ikisi de taranıyor.
   Yeniden derlemek için (proje kökünde):
     npm run css        ya da        ./yayinla.sh
*/
module.exports = {
  content: [
    './_build/sablon/**/*.html',
    './content/**/*.html',
    './content/**/*.md',
    './_build/uret.py',
  ],
  theme: {
    extend: {
      colors: {
        ink:'#1D1D1F', ink2:'#1D1D1F', ink3:'rgba(255,255,255,.18)',
        paper:'#F5F5F7', line:'#D2D2D7', linesoft:'#E8E8ED',
        sea:'var(--accent-ink)', seadeep:'var(--accent-ink)', seasoft:'#F5F5F7',
        sun:'var(--accent)', sundeep:'#6E6E73', sunsoft:'#F5F5F7',
        flag:'#BF4800', flagsoft:'#FFF6F0',
        muted:'#6E6E73', muteddark:'#86868B', text:'#1D1D1F'
      },
      fontFamily: {
        display:['"Inter Tight"','-apple-system','BlinkMacSystemFont','sans-serif'],
        body:['-apple-system','BlinkMacSystemFont','Inter','sans-serif'],
        mono:['-apple-system','BlinkMacSystemFont','Inter','sans-serif']
      },
      maxWidth: { shell:'980px', prose:'692px' }
    }
  },
  plugins: [],
}
