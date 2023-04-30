from typing import List


class Table:
    def __init__(self, data):
        self.swagger_data = data

    def create(self):
        return f"""
              <table class="table">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Name</th>
          <th scope="col">Result(seconds)</th>
        </tr>
      </thead>
      <tbody>
        {self._create_request_data_table()}
      </tbody>
    </table>
               """

    def _create_request_data_table(self) -> str:
        results = self._sort_requests_results(self.swagger_data)
        table_body = []
        for count, res in enumerate(results):
            table_body.append('<thead style="font-style: normal">\n')
            table_body.append(
                f'<tr class="table-{res.get("color")}" style="font-style: normal">\n'
            )
            table_body.append(f'<th scope="col">{count + 1}</th>\n')
            table_body.append(f'<th scope="col">{res.get("name")}</th>\n')
            table_body.append(f'<th scope="col">{str(res.get("results"))[0:5]}</th>\n')
            table_body.append("</tr>\n")
            table_body.append("</thead>\n")
        return "".join(table_body)

    def _sort_requests_results(dself, data: dict) -> List:
        """
        Sort request result
        """
        results = []
        for key, value in data.items():
            if value.get("time_executions") is not None:
                name = f"{value.get('method')} {value.get('path')}"
                avg_time = sum(value.get("time_executions")) / len(
                    value.get("time_executions")
                )
                if avg_time > 3:
                    color = "danger"
                elif avg_time > 1:
                    color = "warning"
                else:
                    color = "light"
                results.append({"name": name, "results": avg_time, "color": color})
        sorted_results = sorted(results, key=lambda d: d["results"], reverse=True)
        return sorted_results
