const app = () => {
  const state = {
    all: [],
    success: [],
    failed: [],
    notAdd: []
  };

  const accordions = document.querySelectorAll('.accordion-item');
  const allButton = document.querySelector('#all');
  const successButton = document.querySelector('#success');
  const failedButton = document.querySelector('#not-checked');
  const notAddButton = document.querySelector('#not-added');
  const accordionsDiv = document.querySelector('#accordions');


  state.all = accordions;
  state.success = Array.from(accordions).filter((item) => {
    const button = item.querySelector('.accordion-header').querySelector('button');
    const status = button.getAttribute('style');
    if (status === 'background-color: #60d891;') {
      return item;
    }
  })

  state.failed = Array.from(accordions).filter((item) => {
    const button = item.querySelector('.accordion-header').querySelector('button');
    const status = button.getAttribute('style');
    if (status === 'background-color: #F47174;') {
      return item;
    }
  })

  state.notAdd= Array.from(accordions).filter((item) => {
    const button = item.querySelector('.accordion-header').querySelector('button');
    const status = button.getAttribute('style');
    if (status === 'background-color: #F56b02;') {
      return item;
    }
  })

  const showBtnHandler = (event) => {
    const element = event.target.parentNode.parentNode.children[1];
    const attribute = element.getAttribute("data-state");
    if (attribute === 'open') {
      element.setAttribute("data-state", "collapsed");
      element.setAttribute("class", "accordion-collapse collapse");
    } else {
      element.setAttribute("data-state", "open");
      element.setAttribute("class", "accordion-collapse open");
    }
  };

  const showAll = () =>  {
    accordionsDiv.innerText = '';
    Array.from(state.all).forEach(element => accordionsDiv.appendChild(element));
  }

  const showSuccess = () => {
    accordionsDiv.innerText = '';
    Array.from(state.success).forEach(element => accordionsDiv.appendChild(element));
  }

  const showFailed = () => {
    accordionsDiv.innerText = '';
    Array.from(state.failed).forEach(element => accordionsDiv.appendChild(element));
  }

  const showNotAdd = () => {
    accordionsDiv.innerText = '';
    Array.from(state.notAdd).forEach(element => accordionsDiv.appendChild(element));
  }

  allButton.addEventListener('click', showAll);
  successButton.addEventListener('click', showSuccess);
  failedButton.addEventListener('click', showFailed);
  notAddButton.addEventListener('click', showNotAdd);
  const accordionArray = Array.from(document.getElementsByClassName('accordion-button'));
  accordionArray.forEach(el => el.addEventListener('click', showBtnHandler));
}

app();
