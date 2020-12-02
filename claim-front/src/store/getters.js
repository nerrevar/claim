export const getCurrentProject = state => state.currentProject

export const getCurrentPage = state => state.currentPage

export const getStartDate = state => {
  if ('' != state.startDate)
    return state.startDate
  else {
    let curr_date = new Date()
    let date_str = '' + curr_date.getFullYear() + '-'
    if (curr_date.getMonth() < 9){
      let month = curr_date.getMonth() + 1
      date_str += '0' + month
    }
    else
      date_str += curr_date.getMonth()
    date_str += '-01'
    return date_str
  }
}

export const getEndDate = state => {
  if ('' != state.endDate)
    return state.endDate
  else {
    let curr_date = new Date()
    let new_date = ''
    if (curr_date.getMonth() <=10)
      new_date = new Date(curr_date.getFullYear(), curr_date.getMonth() + 1, 0)
    else
      new_date = new Date(curr_date.getFullYear(), 0, 0)
    let date_str = '' + new_date.getFullYear() + '-'
    if (new_date.getMonth() < 9){
      let month = new_date.getMonth() + 1
      date_str += '0' + month
    }
    else
      date_str += new_date.getMonth()
    date_str += '-' + new_date.getDate()
    return date_str
  }
}

export const getGroup = state => state.group

export const getQuestion = state => state.question

export const getUser = state => state.user
