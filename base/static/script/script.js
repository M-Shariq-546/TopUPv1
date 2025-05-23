// Catalog Button
console.log('called the js file ')
const catalogBtn = document.getElementById('catalogBtn');
    const dropdownMenu = document.getElementById('dropdownMenu');
  
    catalogBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      dropdownMenu.classList.toggle('show');
    });
  
    document.addEventListener('click', () => {
      dropdownMenu.classList.remove('show');
    });
  
    window.addEventListener('scroll', () => {
      dropdownMenu.classList.remove('show');
    });

    //Mobile Sidebar
    const hamburgerBtn = document.getElementById("hamburgerBtn");
    const sidebar = document.getElementById("sidebar");
    const closeSidebar = document.getElementById("closeSidebar");
  
    hamburgerBtn.addEventListener("click", () => {
      sidebar.classList.add("show");
    });
  
    closeSidebar.addEventListener("click", () => {
      sidebar.classList.remove("show");
    });

  // Cart Toggle
      const cartToggle = document.getElementById('cart-toggle');
      const cartDropdown = document.getElementById('cart-dropdown');
  
      cartToggle?.addEventListener('click', () => {
          cartDropdown?.classList.toggle('hidden');
      });
  
      cartDropdown?.addEventListener('click', (e) => {
          if (e.target.classList.contains('remove-btn')) {
              const item = e.target.closest('.cart-item');
              item.remove();
              updateTotal();
          }
      });
  
      document.querySelector('.clear-btn')?.addEventListener('click', () => {
          document.querySelector('.cart-items').innerHTML = '';
          updateTotal();
      });
  
      function updateTotal() {
          const prices = document.querySelectorAll('.item-price');
          let total = 0;
          prices.forEach(p => {
              const val = parseFloat(p.textContent.replace('$', ''));
              if (!isNaN(val)) total += val;
          });
          document.querySelector('.total-price').textContent = `${total.toFixed(2)} $`;
      }
  
      updateTotal();
  
  
  