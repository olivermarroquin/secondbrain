import org.junit.jupiter.api.Test;
import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;

public class C017_ApiStubTestTest {

  @Test
  void todo() {
    // TODO
    given()
      .when().get("https://example.com")
      .then().statusCode(200);
  }
}
