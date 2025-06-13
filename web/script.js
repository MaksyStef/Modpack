let exportSwitch = document.querySelector('.tabs__export');
let importSwitch = document.querySelector('.tabs__import');

let switchInactive = (e)=> {
  e.target.parentElement.querySelector('.active').classList.remove('active');
  e.target.classList.add('active');
}

exportSwitch.addEventListener('click', switchInactive);
importSwitch.addEventListener('click', switchInactive);
console.log(eel.get_instances())