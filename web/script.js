let exportSwitch = document.querySelector('.tabs__export');
let importSwitch = document.querySelector('.tabs__import');

let switchInactive = (e)=> {
  e.target.parentElement.querySelector('.active').classList.remove('active');
  e.target.classList.add('active');
}

exportSwitch.addEventListener('click', switchInactive);
importSwitch.addEventListener('click', switchInactive);

eel.get_instances()()
  .then((data)=> {
    let dropdownList = document.querySelector('.dropdown__list');
    let dropdownActive = document.querySelector('.dropdown__selected');
    for (const [id, props] of Object.entries(data)) {
      let item = document.createElement('div');
      item.className = "dropdown__item";
      item.setAttribute("data-id", id);
      if (props.icon) { item.setAttribute("data-img", props.icon) };
      item.innerText = props.name;
      dropdownList.appendChild(item);
    }
    dropdownActive.innerHTML = dropdownList.firstElementChild.outerHTML;
    dropdownList.firstElementChild.remove();
  })