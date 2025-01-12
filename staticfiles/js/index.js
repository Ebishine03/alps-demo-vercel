document.addEventListener('DOMContentLoaded', function () {
    const navbar = document.querySelector('.navbar');
  
    const loginIcon = document.querySelector('.login');
    const WishLIstIcon = document.querySelector('.fav-i-l');
    const loginIconLarge = document.querySelector('.login-l .icon-l');
    const searchInput_m=document.querySelector('.search-nav-s');
    const searchInput_l=document.querySelector('.search-nav-l');

    if (!navbar) {
        console.error('Navbar not found!');
        return;
    }

    const staticBasePath = '/static/img/';

    // Function to update navbar and icon styles
    const updateNavbar = () => {
        const isHomepage = window.location.pathname === '/';
        const isScrolled = window.scrollY > 200;

        if (!isHomepage) {
           
            navbar.classList.add('solid');
            updateIcons('solid');
        } else if (isScrolled) {
           
            navbar.classList.add('scrolled');
            navbar.classList.remove('solid');
            updateIcons('scrolled');
        } else {
            // Homepage at the top
            navbar.classList.remove('scrolled', 'solid');
            updateIcons('default');
        }
    };

    // Function to update icons based on class
    const updateIcons = (state) => {
        if (state === 'solid' || state === 'scrolled') {
         
            if (loginIcon) loginIcon.style.backgroundImage = `url('${staticBasePath}user-question-alt-1-svgrepo-com_green.svg')`;
            if (loginIconLarge) loginIconLarge.style.backgroundImage = `url('${staticBasePath}user-question-alt-1-svgrepo-com_green.svg')`;
            if (WishLIstIcon) WishLIstIcon.style.color='black'
            if (searchInput_m) searchInput_m.style.color='black'
            if (searchInput_l) searchInput_l.style.color='black'
           
        } else {
            // Default (homepage top)
         
            if (loginIcon) loginIcon.style.backgroundImage = `url('${staticBasePath}user-question-alt-1-svgrepo-com_white.svg')`;
            if (loginIconLarge) loginIconLarge.style.backgroundImage = `url('${staticBasePath}user-question-alt-1-svgrepo-com_white.svg')`;
            if (WishLIstIcon) WishLIstIcon.style.color='white';
            if (searchInput_m) searchInput_m.style.color='white';
            if (searchInput_l) searchInput_l.style.color='white';
           
        }
    };

    // Event listener for scroll updates
    window.addEventListener('scroll', updateNavbar);

    // Initial check on page load
    updateNavbar();
});
// $(document).ready(function () {
//     $('#itemslider').carousel({ interval: 3000 });
  
//     $('.carousel-showmanymoveone .carousel-item').each(function () {
//       let itemToClone = $(this);
  
//       for (let i = 1; i < 6; i++) {
//         itemToClone = itemToClone.next();
  
//         // Wrap around to the first item if no more siblings exist
//         if (!itemToClone.length) {
//           itemToClone = $(this).siblings(':first');
//         }
  
//         itemToClone.children(':first-child').clone()
//           .addClass(`cloneditem-${i}`)
//           .appendTo($(this));
//       }
// //     });
//   });
  
