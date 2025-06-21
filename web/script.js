let exportSwitch = document.querySelector('.tabs__export');
let importSwitch = document.querySelector('.tabs__import');

let switchInactive = (e)=> {
  e.target.parentElement.querySelector('.active').classList.remove('active');
  e.target.classList.add('active');
}

exportSwitch.addEventListener('click', switchInactive);
importSwitch.addEventListener('click', switchInactive);

const dropdownList = document.querySelector('.dropdown__list');
const dropdownSelected = document.querySelector('.dropdown__selected');

let createDropdownItem = (id, props) => {
  // Create element
  let item = document.createElement('div');
  item.className = "dropdown__item";
  item.setAttribute("data-id", id);
  if (props.icon && props.icon.startsWith("data:image/png;base64,")) { item.setAttribute("data-img", props.icon) }
  else { item.setAttribute("data-img", "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAABg2lDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw1AUhU9TbUVaHOwg4pChOtlFRRxLFYtgobQVWnUweekfNGlIUlwcBdeCgz+LVQcXZ10dXAVB8AfEXXBSdJES70sKLWJ8cHkf571zuO8+QGjVmGr2xQFVs4xMMiHmC6ti8BUBhAGqgMRMPZVdzMFzfd3Dx/e7GM/yvvfnCitFkwE+kTjOdMMi3iCe3bR0zvvEEVaRFOJz4kmDGiR+5Lrs8hvnssMCz4wYucw8cYRYLPew3MOsYqjEM8RRRdUoX8i7rHDe4qzWGqzTJ39hqKitZLlONYYklpBCGiJkNFBFDRZitGukmMjQecLDP+r40+SSyVUFI8cC6lAhOX7wP/g9W7M0PeUmhRJA/4ttf4wDwV2g3bTt72Pbbp8A/mfgSuv66y1g7pP0ZleLHgFD28DFdVeT94DLHWDkSZcMyZH8VEKpBLyf0TcVgOFbYHDNnVvnHKcPQI5mtXwDHBwCE2XKXvd490Dv3P6905nfDx9pcoXDaAH3AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH6QYNAA8DniSA4gAAABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAAI5SURBVHja7d0/a1NRHMfhXJPbxLRp0FaiFDoIOvoWBJe+gs4u/gEHwc0xTuLi4iQq2NW9oIsvwiVgHVyy2FYJJVa9Sep+Hb9DqTzP/us5vXxylnPTFjevtk8agenvRTLeWOuei+YPf2br9zrZ+rN59Pgaq+1s/eMqWz9bnTNPAAJAAAgAASAABIAAEAACQAAIAAEgAP5Xre/TefQD1lea0Xx6n7/Rb57qAxxPsv1f7Gbrn8ycAAgAASAABIAAEAACQAAIAAEgAASAABAA/yh2nz2IvmD+eXwQbWCttxzNX7qQXagvFtn36w8nx9n80TSav3J54ARAAAgAASAABIAAEAACQAAIAAEgAASAAKhrpff5w50P0XxVVdH87tN70Xx/uRPNbw/fRvNlWWbP//aWEwABIAAEgAAQAAJAAAgAASAABIAAEAACoK6V3oePRqNo/taNzTP9ADe7f6L5j5++RPPvXzx2AiAABIAAEAACQAAIAAEgAASAABAAAkAA1BXvntyJ/mB+Z6kVbaDX7ZzqA0jfh5hMf0XzS2Uzmh/vT5wACAABIAAEgAAQAAJAAAgAASAABIAAEAB1xda1dvQ+wKP7d6MNPH/5Kpof9LL79Goe/fqNrz/m0fzwYfb/Dl7vvHECIAAEgAAQAAJAAAgAASAABIAAEAACQADUFdfXW9GF+PmyiDYwWMkaXO1k83sHs2i+DD9CG/3sfYZvRwsnAAJAAAgAASAABIAAEAACQAAIAAEgAARA3V8E51neBiXJXwAAAABJRU5ErkJggg==")}
  item.innerHTML = `<img src="${item.getAttribute("data-img")}" width="16" height="16" /> ${props.name}`;
  
  // Create getProps() method
  item.getProps = ()=> (id, props);
  // Set onClick event listener
  item.addEventListener(
    'click', ()=> {
      if (item in dropdownList.children
            && 
              dropdownList.classList.contains('hidden')) {
        return;
      }
      selectDropdownItem(item);
      dropdownList.classList.toggle('hidden');
    }
  )

  // Append list
  dropdownList.appendChild(item);
}

let selectDropdownItem = (dropdownItem) => {
  // Append method moves an item from Parent_A to Parent_B
  dropdownList.appendChild(dropdownSelected.firstChild)
  dropdownSelected.appendChild(dropdownItem);
}
eel.get_instances()()
  .then((data)=> {
    for (const [id, props] of Object.entries(data)) {
      createDropdownItem(id, props);
    }
    selectDropdownItem(dropdownList.firstElementChild);
  })