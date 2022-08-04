output sqlalchemy_conn {
  value = aws_ssm_parameter.sqlalchemy_conn.value
}

output jdbc_conn {
  value = aws_ssm_parameter.jdbc_conn.value
}