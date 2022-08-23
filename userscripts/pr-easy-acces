// ==UserScript==
// @name        PR - Quick Access
// @namespace   Violentmonkey Scripts
// @match       https://github.com/odoo/odoo/pull/*
// @match       https://github.com/odoo/enterprise/pull/* 
// @exclude-match https://github.com/odoo/odoo/pull/*/files
// @exclude-match https://github.com/odoo/enterprise/pull/*/files
// @grant       none
// @version     1.4
// @author      Yolann Sabaux
// @description Create Buttons to ease access in a PR. 3/28/2022, 3:58:38 PM
// Github: https://github.com/yosa-odoo/odoolbox/blob/main/pr_easy_access.js
// ==/UserScript==

function insertAfter(newNode, existingNode) {
    existingNode.parentNode.insertBefore(newNode, existingNode.nextSibling);
}

function createButton({text, styleB, classesB}) {
    const classes = classesB || []
    const style = styleB || {}
    const button = document.createElement('button')
    button.append(new Text(text || ''))
    Object.entries(style).forEach(([attribute, value]) => button.style[attribute] = value)
    button.classList.add(...classes)
    return button
}

function addEasyAccess(){
  
    // 'Changed Files' button
  const filesButton = createButton({
    text: 'Files Changed',
    styleB: {
      width: '120px',
      left: '15px',
    },
    classesB: ['btn-outline', 'btn-sm', 'btn', 'ml-2']
  })
  
  filesButton.addEventListener('click', (e) => {
    const url = document.URL.concat('/files')
    window.open(url, '_blank').focus();
  })
  
  // 'Copy Branch' button
  const copyButton = createButton({
    text: 'Copy Branch',
    styleB: {
      width: '120px',
      left: '15px',
    },
    classesB: ['btn-outline', 'btn-sm', 'btn', 'ml-2']
  })
  
  copyButton.addEventListener('click', (e) => {
    copyText = document.querySelector('.text-emphasized').text;
    navigator.clipboard.writeText(copyText);
    copyButton.textContent = "Branch copied !";
                        setTimeout(()=>{
                            copyButton.textContent = "Copy Branch";
                        }, 1000)
                    });
  
  // 'Top' Button
  const topButton = createButton({
    text: 'Top',
    styleB: {
      width: '70px',
      left: '50px',
    },
    classesB: ['btn', 'btn-block', 'btn-sm']
  })
  
  topButton.addEventListener('click', (e) => {
    window.scrollTo(0, 300);
  })
  
  // 'Bottom' Button
  const bottomButton = createButton({
    text: 'Bottom',
    styleB: {
      width: '70px',
      left: '60px',
    },
    classesB: ['btn', 'btn-block', 'btn-sm']
  })
  
  bottomButton.addEventListener('click', (e) => {
    window.scrollTo(0, document.body.scrollHeight);
  })
 
  
  // insert buttons
  const title = document.querySelector('.gh-header-number')
  insertAfter(filesButton, title)
  insertAfter(copyButton, filesButton)
  insertAfter(topButton, copyButton)
  insertAfter(bottomButton, topButton)    
  
}

window.addEventListener('load', addEasyAccess)
