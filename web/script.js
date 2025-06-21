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
  if (props.icon) { item.setAttribute("data-img", props.icon) };
  
  item.innerText = props.name;
  
  // Create getProps() method
  item.getProps = ()=> (id, props);
  // Set onClick event listener
  item.addEventListener(
    'click', ()=> selectDropdownItem(item)
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